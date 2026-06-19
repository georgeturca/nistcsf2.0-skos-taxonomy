# Code by georgeturca
# Convert the multilingual NIST CSF 2.0 CSV into an RDF/SKOS Turtle taxonomy.

from pathlib import Path
import re
import pandas
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, SKOS, DCTERMS, RDFS


INPUT_FILE = Path("output/nist_csf2core.csv") # Spreadsheet with the CSF core
REFERENCE_FILE = Path("data/informative_reference_links.csv")# Spreadsheet informative links
OUTPUT_FILE = Path("output/nist_csf2_taxonomy.ttl")
ISO_FILE = Path("data/iso-security.ttl")

#URI prefixes
BASE = Namespace("https://example.org/nist-csf-2.0/")
CSF = Namespace("https://example.org/nist-csf-2.0/concept/")
CSFREF = Namespace("https://example.org/nist-csf-2.0/reference/")



def clean(value):
    if pandas.isna(value):
        return ""
    return str(value).strip()

def normalize_reference(reference):
    reference = " ".join(clean(reference).split())

    # Normalize spaces around parentheses:
    # 4.2 (a) -> 4.2(a)
    reference = re.sub(r"\s+\(", "(", reference)
    reference = re.sub(r"\(\s+", "(", reference)
    reference = re.sub(r"\s+\)", ")", reference)

    # Remove trailing punctuation:
    # 6.1, -> 6.1
    reference = reference.rstrip(",;")

    return reference

def split_implementation_examples(text):
    text = clean(text)

    if not text:
        return []

    examples = re.split(r"(?=Ex\d+:)", text)

    return [example.strip() for example in examples if example.strip()]

def make_safe_id(value):
    """
    Make a value safe for use in a URI.

    Example:
    GV.OC-01 -> GV-OC-01
    SP 800-53 Rev 5.2.0: CM-07(02) -> SP-800-53-Rev-5-2-0-CM-07-02
    """
    value = clean(value)
    value = value.replace(".", "-")
    value = re.sub(r"[^A-Za-z0-9_-]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")

def make_concept_uri(concept_id):
    return CSF[make_safe_id(concept_id)]

def make_reference_uri(reference):
    return CSFREF[make_safe_id(reference)]

def load_reference_links():
    reference_links = {}

    if not REFERENCE_FILE.exists():
        print(f"Warning: reference link file not found: {REFERENCE_FILE}")
        return reference_links

    df = pandas.read_csv(REFERENCE_FILE)

    for index, row in df.iterrows():
        reference = normalize_reference(clean(row.get("reference")))
        label = clean(row.get("label"))
        link = clean(row.get("link"))

        if not reference:
            continue

        reference_links[reference] = {
            "label": label if label else reference,
            "link": link,
        }

    return reference_links

def add_multilingual_literals(graph, concept_uri, row, column_prefix, predicate):
# Convert columns like skos:prefLabel @en, @fr, @de
    for column in row.index:
        if not column.startswith(column_prefix + "_"):
            continue

        language = column.replace(column_prefix + "_", "")
        value = clean(row[column])

        if value:
            graph.add((concept_uri, predicate, Literal(value, lang=language)))

# Load the ISO 27001 taxonomy to enable linking CSF controls to ISO clauses and controls.
def load_iso_lookup():
    iso_lookup = {
        "clauses": {},
        "annex_controls": {},
    }

    if not ISO_FILE.exists():
        print(f"Warning: ISO taxonomy file not found: {ISO_FILE}")
        return iso_lookup

    iso_graph = Graph()
    iso_graph.parse(ISO_FILE, format="turtle")

    for concept in iso_graph.subjects(RDF.type, SKOS.Concept):
        concept_uri = str(concept)

        for notation in iso_graph.objects(concept, SKOS.notation):
            notation = str(notation)

            if "/27001/clause/" in concept_uri:
                iso_lookup["clauses"][notation] = concept

            elif "/27001/control/" in concept_uri:
                iso_lookup["annex_controls"][notation] = concept

                if notation.startswith("A."):
                    iso_lookup["annex_controls"][notation[2:]] = concept

    return iso_lookup


# Try to find a matching ISO clause or control URI for a given informative reference string.
def find_iso_reference_uri(reference, iso_lookup):
    if not reference.startswith("ISO/IEC 27001:2022:"):
        return None

    if "Annex A Controls:" in reference:
        control_id = reference.split("Annex A Controls:", 1)[1].strip().strip(",")

        if not control_id or control_id.lower() == "none":
            return None

        return iso_lookup["annex_controls"].get(control_id)

    if "Mandatory Clause:" in reference:
        clause_id = reference.split("Mandatory Clause:", 1)[1].strip().strip(",")

        if not clause_id or clause_id.lower() == "none":
            return None

        return iso_lookup["clauses"].get(clause_id)

    return None


def add_informative_references(graph, concept_uri, informative_references, reference_links, reference_scheme, iso_lookup):
    informative_references = clean(informative_references)

    if not informative_references:
        return

    for line in informative_references.splitlines():
        reference = normalize_reference(line)

        if not reference:
            continue

        reference_data = reference_links.get(reference, {})
        label = reference_data.get("label", reference)
        link = reference_data.get("link", "")

        reference_uri = make_reference_uri(reference)

        # Always create a local informative reference concept.
        graph.add((reference_uri, RDF.type, SKOS.Concept))
        graph.add((reference_uri, SKOS.inScheme, reference_scheme))
        graph.add((reference_uri, DCTERMS.type, Literal("InformativeReference")))
        graph.add((reference_uri, SKOS.prefLabel, Literal(label, lang="en")))
        
        if not list(graph.objects(reference_uri, SKOS.notation)):
        graph.add((reference_uri, SKOS.notation, Literal(reference)))

        # Main semantic relation: the NIST CSF concept references this informative reference.
        graph.add((concept_uri, DCTERMS.references, reference_uri))

        # Browser-friendly relation for local navigation.
        graph.add((concept_uri, SKOS.related, reference_uri))
        graph.add((reference_uri, SKOS.related, concept_uri))

        # External webpage if available.
        if link:
            graph.add((reference_uri, RDFS.seeAlso, URIRef(link)))

        # If this reference matches Ion's ISO taxonomy, link the reference concept to it.
        iso_uri = find_iso_reference_uri(reference, iso_lookup)

        if iso_uri:
            graph.add((reference_uri, SKOS.exactMatch, iso_uri))

def print_summary(graph, scheme):
    print(f"Created {OUTPUT_FILE}")
    print(f"RDF triples: {len(graph)}")
    print()
    print("Function/category tree:")

    functions = sorted(
        graph.objects(scheme, SKOS.hasTopConcept),
        key=lambda uri: str(next(graph.objects(uri, SKOS.notation), uri)),
    )

    for function_uri in functions:
        function_id = next(graph.objects(function_uri, SKOS.notation), "")
        function_label = next(graph.objects(function_uri, SKOS.prefLabel), "")

        print(f"- {function_id} {function_label}")

        categories = sorted(
            graph.objects(function_uri, SKOS.narrower),
            key=lambda uri: str(next(graph.objects(uri, SKOS.notation), uri)),
        )

        for category_uri in categories:
            category_type = str(next(graph.objects(category_uri, DCTERMS.type), ""))

            if category_type != "Category":
                continue

            category_id = next(graph.objects(category_uri, SKOS.notation), "")
            category_label = next(graph.objects(category_uri, SKOS.prefLabel), "")

            print(f"  - {category_id} {category_label}")

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Could not find input CSV: {INPUT_FILE}")

    df = pandas.read_csv(INPUT_FILE)
    reference_links = load_reference_links()
    iso_lookup = load_iso_lookup()

    graph = Graph()

    graph.bind("skos", SKOS)
    graph.bind("dcterms", DCTERMS)
    graph.bind("rdfs", RDFS)
    graph.bind("csf", CSF)
    graph.bind("csfref", CSFREF)

    scheme = BASE["scheme/core"]

    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal("NIST Cybersecurity Framework 2.0 Core", lang="en")))
    graph.add((scheme, DCTERMS.title, Literal("NIST Cybersecurity Framework 2.0 Core", lang="en")))
    graph.add((scheme, DCTERMS.source, Literal("NIST CSF 2.0 Reference Tool", lang="en")))

    reference_scheme = BASE["scheme/informative-references"]

    graph.add((reference_scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((reference_scheme, SKOS.prefLabel, Literal("NIST CSF 2.0 Informative References", lang="en")))
    graph.add((reference_scheme, DCTERMS.title, Literal("NIST CSF 2.0 Informative References", lang="en")))
    graph.add((reference_scheme, DCTERMS.source, Literal("NIST CSF 2.0 Reference Tool", lang="en")))


    known_ids = set(df["id"].dropna().astype(str))

    for index, row in df.iterrows():
        concept_id = clean(row.get("id"))
        concept_type = clean(row.get("type"))

        if not concept_id:
            continue

        concept_uri = make_concept_uri(concept_id)

        graph.add((concept_uri, RDF.type, SKOS.Concept))
        graph.add((concept_uri, SKOS.inScheme, scheme))
        graph.add((concept_uri, SKOS.notation, Literal(concept_id)))
        graph.add((concept_uri, DCTERMS.type, Literal(concept_type)))

        add_multilingual_literals(
            graph=graph,
            concept_uri=concept_uri,
            row=row,
            column_prefix="label",
            predicate=SKOS.prefLabel,
        )

        add_multilingual_literals(
            graph=graph,
            concept_uri=concept_uri,
            row=row,
            column_prefix="description",
            predicate=SKOS.definition,
        )

        implementation_examples = clean(row.get("implementation_examples"))
        
        for example in split_implementation_examples(implementation_examples):
            graph.add((
                concept_uri,
                SKOS.example,
                Literal(example, lang="en")
            ))

        add_informative_references(
            graph=graph,
            concept_uri=concept_uri,
            informative_references=row.get("informative_references"),
            reference_links=reference_links,
            reference_scheme=reference_scheme,
            iso_lookup=iso_lookup,
        )

        if concept_type == "Function":
            graph.add((scheme, SKOS.hasTopConcept, concept_uri))
            graph.add((concept_uri, SKOS.topConceptOf, scheme))

    #Hierarchy
    for index, row in df.iterrows():
        concept_id = clean(row.get("id"))
        parent_id = clean(row.get("parent_id"))

        if not concept_id or not parent_id:
            continue

        if parent_id not in known_ids:
            #print(f"Warning: parent {parent_id} for {concept_id} was not found in CSV")
            continue

        child_uri = make_concept_uri(concept_id)
        parent_uri = make_concept_uri(parent_id)

        graph.add((child_uri, SKOS.broader, parent_uri))
        graph.add((parent_uri, SKOS.narrower, child_uri))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=OUTPUT_FILE, format="turtle")

    print_summary(graph, scheme)

if __name__ == "__main__":
    main()