#Code by georgeturca
#Take the NIST CSF 2.0 .xlsx(csv) and create a clean CSV | Multilanguage, for english-only use src/extract_csf_core.py

from pathlib import Path
import re
import pandas

INPUT_FOLDER = Path("data/csf/languages")
OUTPUT_FILE = Path("output/nist_csf2core.csv")
LANGUAGE_FILES = {
    "en": {"file": "csf2_en_english.xlsx", "sheet": "CSF 2.0"},
    "fr": {"file": "csf2_fr_french.xlsx", "sheet": "French"},
    "de": {"file": "csf2_de_german.xlsx", "sheet": "German"},
    "el": {"file": "csf2_el_greek.xlsx", "sheet": "Greek"},
    "ja": {"file": "csf2_ja_japanese.xlsx", "sheet": "Japanese"},
    "ko": {"file": "csf2_ko_korean.xlsx", "sheet": "Korean"},
    "zh": {"file": "csf2_zh_mandarin.xlsx", "sheet": "Chinese"},
    "no": {"file": "csf2_no_norwegian.xlsx", "sheet": "Norwegian"},
    "pl": {"file": "csf2_pl_polish.xlsx", "sheet": "Polish"},
    "pt": {"file": "csf2_pt_portugese.xlsx", "sheet": "Portuguese"},
    "es": {"file": "csf2_es_spanish.xlsx", "sheet": "Spanish"},
    "th": {"file": "csf2_th_thai.xlsx", "sheet": "Thai"},
}

FUNCTION_RE = re.compile(
    r"^(?P<label>.*?)\s*\((?P<id>[A-Z]{2})\)\s*[:：]\s*(?P<description>.*)$" #GOVERN (GV): The organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored
)

CATEGORY_RE = re.compile(
    r"^(?P<label>.*?)\s*\((?P<id>[A-Z]{2}\.[A-Z]{2})\)\s*[:：]\s*(?P<description>.*)$" #Organizational Context (GV.OC): The circumstances - mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements - surrounding the organization's cybersecurity risk management decisions are understood
)

SUBCATEGORY_RE = re.compile(
    r"^(?P<id>[A-Z]{2}\.[A-Z]{2}-\d{2})\s*[:：]\s*(?P<description>.*)$" #GV.OC-01: The organizational mission is understood and informs cybersecurity risk management
)

WITHDRAWN_PREFIX = "[Withdrawn:"


def clean(value):
    if pandas.isna(value):
        return ""
    return str(value).replace("\r\n", "\n").strip()

def parse_row(row):
    function_text = clean(row.iloc[0])
    category_text = clean(row.iloc[1])
    subcategory_text = clean(row.iloc[2])
    implementation_examples = clean(row.iloc[3])
    informative_references = clean(row.iloc[4])

    if function_text:
        match = FUNCTION_RE.match(function_text)

        if match:
            return {
                "id": match.group("id").strip(),
                "type": "Function",
                "label": match.group("label").strip(),
                "description": match.group("description").strip(),
                "implementation_examples": implementation_examples,
                "informative_references": informative_references,
            }

    if category_text:
        match = CATEGORY_RE.match(category_text)

        if match:
            return {
                "id": match.group("id").strip(),
                "type": "Category",
                "label": match.group("label").strip(),
                "description": match.group("description").strip(),
                "implementation_examples": implementation_examples,
                "informative_references": informative_references,
            }

    if subcategory_text:
        match = SUBCATEGORY_RE.match(subcategory_text)

        if match:
            description = match.group("description").strip()
            subcategory_id = match.group("id").strip()

            return {
                "id": subcategory_id,
                "type": "Subcategory",
                "label": subcategory_id,
                "description": description,
                "implementation_examples": implementation_examples,
                "informative_references": informative_references,
            }

    return None

def add_language_data(concepts, concept, language, parent_id):
    concept_id = concept["id"]

    if concept_id not in concepts:
        concepts[concept_id] = {
            "id": concept_id,
            "parent_id": parent_id,
            "type": concept["type"],
            "implementation_examples": "",
            "informative_references": "",
        }

    concepts[concept_id]["parent_id"] = parent_id
    concepts[concept_id]["type"] = concept["type"]

    # Multilingual fields
    concepts[concept_id][f"label_{language}"] = concept["label"]
    concepts[concept_id][f"description_{language}"] = concept["description"]

    # English-only fields
    if language == "en":
        concepts[concept_id]["implementation_examples"] = concept["implementation_examples"]
        concepts[concept_id]["informative_references"] = concept["informative_references"]

    

# We extract the structure of NIST CSF 2.0 from the english reference tool as informative references are more full and the rest of translations are just incomplete translation of the english one.
def extract_structure():
    file_path = INPUT_FOLDER / LANGUAGE_FILES["en"]["file"]
    df = pandas.read_excel(file_path, sheet_name=LANGUAGE_FILES["en"]["sheet"], header=1).iloc[:, 0:5]
    
    active_ids = set()
    withdrawn_ids = set()
    parent_by_id = {}
    type_by_id = {}

    current_function_id = ""
    current_category_id = ""
    current_category_is_withdrawn = False
    
    for index, row in df.iterrows():
        concept = parse_row(row)

        if concept is None:
            continue

        concept_id = concept["id"]
        concept_type = concept["type"]
        description = concept["description"]

        if concept_type == "Function":
            parent_id = ""
            withdrawn = description.startswith(WITHDRAWN_PREFIX)

            current_function_id = concept_id
            current_category_id = ""
            current_category_is_withdrawn = withdrawn

        elif concept_type == "Category":
            parent_id = current_function_id
            withdrawn = description.startswith(WITHDRAWN_PREFIX)

            current_category_id = concept_id
            current_category_is_withdrawn = withdrawn

        else:
            parent_id = current_category_id
            withdrawn = (
                current_category_is_withdrawn
                or description.startswith(WITHDRAWN_PREFIX)
            )

        parent_by_id[concept_id] = parent_id
        type_by_id[concept_id] = concept_type

        if withdrawn:
            withdrawn_ids.add(concept_id)
        else:
            active_ids.add(concept_id)

    return active_ids, withdrawn_ids, parent_by_id, type_by_id

def extract_language(language, config, concepts, active_ids, parent_by_id):
    file_path = INPUT_FOLDER / config["file"]
    df = pandas.read_excel(file_path, sheet_name=config["sheet"], header=1).iloc[:, 0:5]

    for index, row in df.iterrows():
        concept = parse_row(row)

        if concept is None:
            continue

        concept_id = concept["id"]

        # Only keep concepts that English marked as active.
        if concept_id not in active_ids:
            continue

        parent_id = parent_by_id.get(concept_id, "")
        add_language_data(concepts, concept, language, parent_id)


def print_summary(output_df, active_ids, withdrawn_ids):
    print()
    print(f"Created {OUTPUT_FILE}")
    print(f"Rows: {len(output_df)}")
    print(f"Columns: {len(output_df.columns)}")
    print(f"Languages: {', '.join(LANGUAGE_FILES.keys())}")
    print(f"Active concepts: {len(active_ids)}")
    print(f"Withdrawn concepts ignored: {len(withdrawn_ids)}")
    print()
    print("Concept counts:")
    print(output_df["type"].value_counts().to_string())
    print()



def main():
    active_ids, withdrawn_ids, parent_by_id, type_by_id = extract_structure()
    concepts = {}

    for language, config in LANGUAGE_FILES.items():
        extract_language(
            language=language,
            config=config,
            concepts=concepts,
            active_ids=active_ids,
            parent_by_id=parent_by_id,
        )

    output_df = pandas.DataFrame(concepts.values())
    output_df.to_csv(OUTPUT_FILE, index=False)

    print_summary(output_df, active_ids, withdrawn_ids)

if __name__ == "__main__":
    main()
