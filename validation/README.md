# SRQ2 SPARQL validation package

This folder contains SPARQL queries for the 34 NIST CSF 2.0 competency questions.

## Purpose

Use this package to answer:

> SRQ2: Does the resulting SKOS taxonomy provide correct answers to competency questions when queried with SPARQL?

A CQ passes when the query result matches the expected answer in your competency-question table.

## Important model check

Your intended model is:

```text
NIST CSF concept -> dcterms:references -> local informative reference concept
local ISO reference concept -> skos:exactMatch -> Ion's ISO taxonomy concept
```

Before running the ISO/reference questions, run:

```bash
python run_cq_queries.py --data output/nist_csf2_taxonomy.ttl --queries queries --out results
```

Then open:

```text
results/check_reference_model.csv
```

You should see:
- `dcterms:references triples` greater than 0
- `skos:exactMatch triples` greater than 0

If either is 0, rebuild your taxonomy with the updated `build_taxonomy.py`.

## How to run on your project

From your project root:

```bash
cd ~/Media/University/MOD12/nistcsf2.0-skos-taxonomy
source .venv/bin/activate
python src/build_project.py
```

Stop the browser server if it starts, or open a second terminal.

Copy this validation folder into your project, then run:

```bash
python validation/run_cq_queries.py   --data output/nist_csf2_taxonomy.ttl   --queries validation/queries   --out validation/results
```

## How to verify manually

1. Open `validation/results/summary.csv`.
2. Check that every query has status `OK`.
3. Open each CQ result CSV.
4. Compare the returned `notation` values with the expected answer in your competency-question table.
5. For CQ21-CQ24, check that references are returned through `dcterms:references`.
6. For CQ27-CQ29, check that ISO mappings are returned through `skos:exactMatch`.

## What if a query returns 0 rows?

- If direct hierarchy questions return 0 rows, check the concept URI, e.g. `GV.OC` becomes `csf:GV-OC`.
- If reference questions return 0 rows, your Turtle file probably still uses only `skos:related` and was not rebuilt after changing back to `dcterms:references`.
- If ISO questions return 0 rows, check that `data/iso-security.ttl` exists before rebuilding the taxonomy.

## Files

- `queries/cq01_...rq` to `queries/cq34_...rq`: one query per competency question.
- `queries/check_reference_model.rq`: sanity check for references and ISO mappings.
- `cq_query_summary.csv`: overview of all queries.
- `all_cq_sparql_queries.md`: all queries in one readable Markdown file.
- `run_cq_queries.py`: Python runner using RDFLib.
