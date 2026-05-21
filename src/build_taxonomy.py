# Code by georgeturca
# Convert the multilingual NIST CSF 2.0 CSV into an RDF/SKOS Turtle taxonomy.

from pathlib import Path
import re
import pandas
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, SKOS, DCTERMS, RDFS


INPUT_FILE = Path("data/nist_csf2core_multilang.csv") # Spreadsheet with the CSF core
REFERENCE_FILE = Path("data/informative_reference_links_filled.csv")# Spreadsheet informative links
OUTPUT_FILE = Path("docs/nist_csf2_taxonomy.ttl")


BASE = Namespace("https://example.org/nist-csf-2.0/")
CSF = Namespace("https://example.org/nist-csf-2.0/concept/")



def clean(value):
    if pandas.isna(value):
        return ""
    return str(value).strip()

def normalize_reference(reference):
    return " ".join(reference.strip().split())

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

def load_reference_links():
    reference_links = {}
    df = pandas.read_csv(REFERENCE_FILE)

    if not REFERENCE_FILE.exists():
        print(f"Warning: reference link file not found: {REFERENCE_FILE}")
        return reference_links

    for index, row in df.iterrows():
        reference = normalize_reference(clean(row.get("reference")))
        link = clean(row.get("link"))

        if not reference:
            continue

        reference_links[reference] = link

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


def add_informative_references(graph, concept_uri, informative_references, reference_links):
    informative_references = clean(informative_references)

    if not informative_references:
        return

    for line in informative_references.splitlines():
        reference = normalize_reference(line)

        if not reference:
            continue

        # Add each informative reference as a separate scope note.
        graph.add((
            concept_uri,
            SKOS.scopeNote,
            Literal(reference)
        ))

        link = reference_links.get(reference, "")

        if not link:
            continue

        graph.add((concept_uri, RDFS.seeAlso, URIRef(link)))

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Could not find input CSV: {INPUT_FILE}")

    df = pandas.read_csv(INPUT_FILE)
    reference_links = load_reference_links()

    graph = Graph()

    graph.bind("skos", SKOS)
    graph.bind("dcterms", DCTERMS)
    graph.bind("rdfs", RDFS)
    graph.bind("csf", CSF)

    scheme = BASE["scheme/core"]

    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal("NIST Cybersecurity Framework 2.0 Core", lang="en")))
    graph.add((scheme, DCTERMS.title, Literal("NIST Cybersecurity Framework 2.0 Core", lang="en")))
    graph.add((scheme, DCTERMS.source, Literal("NIST CSF 2.0 Reference Tool", lang="en")))

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

if __name__ == "__main__":
    main()