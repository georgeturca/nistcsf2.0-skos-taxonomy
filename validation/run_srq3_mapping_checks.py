from pathlib import Path
from rdflib import Graph
import csv

DATA_FILE = Path("output/nist_csf2_taxonomy.ttl")
QUERY_DIR = Path("validation/srq3_mapping_queries")
RESULTS_DIR = Path("validation/results/srq3_mapping")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CHECKS = {
    "m01_iso_mapping_count.rq": {
        "description": "ISO mappings are present",
        "expected": "Mapping count greater than 0",
        "mode": "single_count_greater_than_zero",
    },
    "m02_invalid_iso_targets.rq": {
        "description": "All ISO mappings point to Ion's ISO taxonomy namespace",
        "expected": "0 rows",
        "mode": "zero_rows",
    },
    "m03_invalid_mapping_subjects.rq": {
        "description": "All ISO mappings start from informative reference concepts",
        "expected": "0 rows",
        "mode": "zero_rows",
    },
    "m04_nist_to_iso_navigation.rq": {
        "description": "NIST concepts can be navigated to ISO concepts",
        "expected": "Rows returned",
        "mode": "rows_greater_than_zero",
    },
    "m05_iso_to_nist_navigation.rq": {
        "description": "ISO concepts can be navigated back to NIST concepts",
        "expected": "Rows returned",
        "mode": "rows_greater_than_zero",
    },
}


def evaluate_check(results, mode):
    if mode == "zero_rows":
        return len(results) == 0

    if mode == "rows_greater_than_zero":
        return len(results) > 0

    if mode == "single_count_greater_than_zero":
        if len(results) != 1:
            return False
        try:
            return int(results[0][0]) > 0
        except Exception:
            return False

    return False


def write_results_csv(query_name, results):
    output_file = RESULTS_DIR / f"{Path(query_name).stem}.csv"

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not results:
            writer.writerow(["No results"])
            return output_file

        labels = [str(label) for label in results[0].labels]
        writer.writerow(labels)

        for row in results:
            writer.writerow([str(value) for value in row])

    return output_file


def main():
    print("SRQ3 mapping validation results")
    print("=" * 40)
    print()

    graph = Graph()
    graph.parse(DATA_FILE, format="turtle")

    summary_rows = []
    all_passed = True

    for query_name, check in CHECKS.items():
        query_file = QUERY_DIR / query_name

        if not query_file.exists():
            status = "FAIL"
            actual = "query file not found"
            result_file = ""

            all_passed = False

            print(f"Check: {query_name}")
            print(f"Description: {check['description']}")
            print(f"Expected: {check['expected']}")
            print(f"Actual: {actual}")
            print(f"Status: {status}")
            print()

            summary_rows.append({
                "check": query_name,
                "description": check["description"],
                "expected": check["expected"],
                "actual": actual,
                "status": status,
                "result_file": result_file,
            })

            continue

        query_text = query_file.read_text(encoding="utf-8")
        results = list(graph.query(query_text))

        passed = evaluate_check(results, check["mode"])
        status = "PASS" if passed else "FAIL"

        if not passed:
            all_passed = False

        result_file = write_results_csv(query_name, results)

        if check["mode"] == "single_count_greater_than_zero" and results:
            actual = str(results[0][0])
        else:
            actual = f"{len(results)} rows"

        print(f"Check: {query_name}")
        print(f"Description: {check['description']}")
        print(f"Expected: {check['expected']}")
        print(f"Actual: {actual}")
        print(f"Status: {status}")

        if results:
            print("Sample results:")
            for row in results[:5]:
                print("  " + " | ".join(str(value) for value in row))

        print()

        summary_rows.append({
            "check": query_name,
            "description": check["description"],
            "expected": check["expected"],
            "actual": actual,
            "status": status,
            "result_file": str(result_file),
        })

    summary_file = RESULTS_DIR / "summary.csv"

    with summary_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "check",
                "description",
                "expected",
                "actual",
                "status",
                "result_file",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    report_file = RESULTS_DIR / "srq3_mapping_report.txt"

    with report_file.open("w", encoding="utf-8") as f:
        f.write("SRQ3 mapping validation results\n")
        f.write("=" * 40 + "\n\n")

        for row in summary_rows:
            f.write(f"Check: {row['check']}\n")
            f.write(f"Description: {row['description']}\n")
            f.write(f"Expected: {row['expected']}\n")
            f.write(f"Actual: {row['actual']}\n")
            f.write(f"Status: {row['status']}\n")
            f.write(f"Result file: {row['result_file']}\n\n")

        f.write("=" * 40 + "\n")
        f.write(f"Overall status: {'PASS' if all_passed else 'FAIL'}\n")

    print("=" * 40)
    print(f"Overall status: {'PASS' if all_passed else 'FAIL'}")
    print()
    print(f"Summary saved to: {summary_file}")
    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()
