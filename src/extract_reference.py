# Code by georgeturca
# Extract unique informative references from the NIST CSF multilingual CSV

from pathlib import Path
import pandas


INPUT_FILE = Path("data/nist_csf2core_multilang.csv")
OUTPUT_FILE = Path("data/informative_reference_links.csv")

def clean(value):
    if pandas.isna(value):
        return ""
    return str(value).strip()


def normalize_reference(reference):
    return " ".join(reference.strip().split())


def split_reference(reference):
    #'SCF: BCD-01' -> source = 'SCF', reference_id = 'BCD-01'
    if ":" not in reference:
        return reference, ""

    source, reference_id = reference.split(":", 1)

    return source.strip(), reference_id.strip()


def main():
    df = pandas.read_csv(INPUT_FILE)
    unique_references = set()

    for value in df["informative_references"]:
        text = clean(value)

        if not text:
            continue

        for line in text.splitlines():
            reference = normalize_reference(line)

            if reference:
                unique_references.add(reference)

    rows = []

    for reference in sorted(unique_references):
        source, reference_id = split_reference(reference)

        rows.append({
            "reference": reference,
            "source": source,
            "reference_id": reference_id,
            "label": reference,
            "link": "",
        })

    output_df = pandas.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    main()