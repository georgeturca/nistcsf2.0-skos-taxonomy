#!/usr/bin/env python3
"""
Run all SRQ2 competency-question SPARQL queries against a Turtle file.

Usage:
  python validation/run_cq_queries.py --data output/nist_csf2_taxonomy.ttl
  python validation/run_cq_queries.py --data /path/to/nist_csf2_taxonomy.ttl --queries validation/queries --out validation/results

This script writes:
  - one CSV result file per query
  - summary.csv with row counts and errors
"""
from pathlib import Path
import argparse
import csv
from rdflib import Graph
from rdflib.query import ResultRow

def cell_to_str(value):
    if value is None:
        return ""
    return str(value)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to the Turtle taxonomy file.")
    parser.add_argument("--queries", default="queries", help="Folder containing .rq files.")
    parser.add_argument("--out", default="results", help="Output folder for CSV results.")
    args = parser.parse_args()

    data_path = Path(args.data)
    queries_dir = Path(args.queries)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Cannot find data file: {data_path}")
    if not queries_dir.exists():
        raise FileNotFoundError(f"Cannot find query folder: {queries_dir}")

    print(f"Loading RDF graph: {data_path}")
    graph = Graph()
    graph.parse(data_path, format="turtle")
    print(f"Loaded triples: {len(graph)}")

    summary = []

    for query_file in sorted(queries_dir.glob("*.rq")):
        query_text = query_file.read_text(encoding="utf-8")
        result_csv = out_dir / (query_file.stem + ".csv")

        try:
            results = graph.query(query_text)
            vars_ = [str(v) for v in results.vars]
            rows = list(results)

            with result_csv.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(vars_)
                for row in rows:
                    writer.writerow([cell_to_str(row.get(v)) for v in results.vars])

            summary.append({
                "query": query_file.name,
                "status": "OK",
                "rows": len(rows),
                "result_file": str(result_csv),
                "error": "",
            })
            print(f"{query_file.name}: OK ({len(rows)} rows)")

        except Exception as exc:
            summary.append({
                "query": query_file.name,
                "status": "ERROR",
                "rows": 0,
                "result_file": "",
                "error": str(exc),
            })
            print(f"{query_file.name}: ERROR: {exc}")

    summary_file = out_dir / "summary.csv"
    with summary_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["query", "status", "rows", "result_file", "error"])
        writer.writeheader()
        writer.writerows(summary)

    print()
    print(f"Summary written to: {summary_file}")

    # Useful warning for the NIST-reference/ISO-linking model.
    check_rows = [row for row in summary if row["query"] == "check_reference_model.rq"]
    if check_rows and check_rows[0]["status"] == "OK":
        print("Open results/check_reference_model.csv to confirm dcterms:references and skos:exactMatch counts.")

if __name__ == "__main__":
    main()
