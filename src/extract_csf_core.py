#Code by georgeturca
#Take the NIST CSF 2.0 .xlsx(csv) and create a clean CSV

from pathlib import Path
import re
import pandas
import csv

INPUT_FILE = Path("data/csf2.xlsx")
OUTPUT_FILE = Path("data/nist_csf2core.csv")
SHEET_NAME = "CSF 2.0"

FUNCTION_RE = re.compile(
    r"^(?P<label>.*?)\s*\((?P<id>[A-Z]{2})\):\s*(?P<description>.*)$" #GOVERN (GV): The organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored
)

CATEGORY_RE = re.compile(
    r"^(?P<label>.*?)\s*\((?P<id>[A-Z]{2}\.[A-Z]{2})\):\s*(?P<description>.*)$" #Organizational Context (GV.OC): The circumstances - mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements - surrounding the organization's cybersecurity risk management decisions are understood
)

SUBCATEGORY_RE = re.compile(
    r"^(?P<id>[A-Z]{2}\.[A-Z]{2}-\d{2}):\s*(?P<description>.*)$" #GV.OC-01: The organizational mission is understood and informs cybersecurity risk management
)



def clean(value):
    if pandas.isna(value):
        return ""
    return str(value).strip()

def add_row(rows, concept_id, parent_id, concept_type, label, description,
            implementation_examples="", informative_references=""):
    rows.append({
        "id": concept_id,
        "parent_id": parent_id,
        "type": concept_type,
        "label": label,
        "description": description,
        "implementation_examples": implementation_examples,
        "informative_references": informative_references,
    })

def main():
    df = pandas.read_excel(INPUT_FILE, sheet_name=SHEET_NAME, header=1)

    rows = []

    current_function_id = ""
    current_category_id = ""

    for index, row in df.iterrows():
        function_text = clean(row.get("Function"))
        category_text = clean(row.get("Category"))
        subcategory_text = clean(row.get("Subcategory"))
        implementation_examples = clean(row.get("Implementation Examples"))
        informative_references = clean(row.get("Informative References"))


        if function_text:
            match = FUNCTION_RE.match(function_text)

            # If rows only say "GOVERN (GV)" (doesnt match) - ignore.
            if match:
                function_id = match.group("id").strip() #GV
                label = match.group("label").strip().title() #GOVERN
                description = match.group("description").strip() # The organization's cybersecurity.....

                add_row(rows, function_id, "", "Function", label, description, implementation_examples, informative_references)

                current_function_id = function_id
                current_category_id = ""
                current_category_is_withdrawn = False

        WITHDRAWN_PREFIX = "[Withdrawn:"

        if category_text:
            match = CATEGORY_RE.match(category_text)

            if match:
                category_id = match.group("id").strip() #GV.OC
                label = match.group("label").strip().title() # Organizational Context
                description = match.group("description").strip() # The circumstances - mission, stakeholder expectations, dependencies, and lega....
                current_category_id = category_id
                if not description.startswith(WITHDRAWN_PREFIX):
                    add_row(rows, category_id, current_function_id, "Category", label, description, implementation_examples, informative_references)

        if subcategory_text:
            match = SUBCATEGORY_RE.match(subcategory_text)

            if match:
                subcategory_id = match.group("id").strip() # GV.OC-01
                description = match.group("description").strip() # The organizational mission is understood and informs cybersecurity risk management
                if not label.startswith(WITHDRAWN_PREFIX):
                    add_row(rows, subcategory_id, current_category_id, "Subcategory", "", description, implementation_examples, informative_references)


    output_df = pandas.DataFrame(rows)
    output_df.to_csv(OUTPUT_FILE, index=False)
        

if __name__ == "__main__":
    main()
