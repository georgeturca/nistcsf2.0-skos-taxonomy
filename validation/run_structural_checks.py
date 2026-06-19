from pathlib import Path
from rdflib import Graph

DATA_FILE = Path("output/nist_csf2_taxonomy.ttl")
QUERY_DIR = Path("validation/structural_queries")
RESULTS_DIR = Path("validation/results")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CHECKS = {
    "missing_english_labels.rq": {
        "description": "Every core concept has an English skos:prefLabel",
        "expected": "0 rows",
        "mode": "zero_rows",
    },
    "duplicate_notations.rq": {
        "description": "No duplicate skos:notation values exist within the same scheme",
        "expected": "0 rows",
        "mode": "zero_rows",
    },
    "reference_counts.rq": {
        "description": "Reference model contains dcterms:references, informative reference concepts, and ISO exactMatch links",
        "expected": "All counts greater than 0",
        "mode": "counts_greater_than_zero",
    },
}

g = Graph()
g.parse(DATA_FILE, format="turtle")

summary_lines = []
summary_lines.append("Structural validation query results")
summary_lines.append("=" * 40)
summary_lines.append("")

all_passed = True

for query_name, info in CHECKS.items():
    query_path = QUERY_DIR / query_name

    if not query_path.exists():
        all_passed = False
        summary_lines.append(f"{query_name}: FAIL")
        summary_lines.append(f"Reason: query file not found: {query_path}")
        summary_lines.append("")
        continue

    results = list(g.query(query_path.read_text()))

    if info["mode"] == "zero_rows":
        passed = len(results) == 0
    elif info["mode"] == "counts_greater_than_zero":
        passed = len(results) > 0 and all(int(row[1]) > 0 for row in results)
    else:
        passed = False

    if not passed:
        all_passed = False

    summary_lines.append(f"Check: {query_name}")
    summary_lines.append(f"Description: {info['description']}")
    summary_lines.append(f"Expected: {info['expected']}")
    summary_lines.append(f"Actual rows: {len(results)}")
    summary_lines.append(f"Status: {'PASS' if passed else 'FAIL'}")

    if results:
        summary_lines.append("Results:")
        for row in results:
            summary_lines.append("  " + " | ".join(str(value) for value in row))

    summary_lines.append("")

summary_lines.append("=" * 40)
summary_lines.append(f"Overall status: {'PASS' if all_passed else 'FAIL'}")

report = "\n".join(summary_lines)

print(report)

output_file = RESULTS_DIR / "structural_sparql_report.txt"
output_file.write_text(report, encoding="utf-8")

print()
print(f"Saved report to: {output_file}")
