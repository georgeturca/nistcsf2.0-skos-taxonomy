# Validation

This folder contains the validation material for the NIST CSF 2.0 SKOS taxonomy. It is used to check whether the generated RDF/Turtle file is structurally consistent, whether it can answer the competency questions, and whether the ISO/IEC 27001 mapping model works as expected.

The validation supports two main parts of the research:

* **SRQ2:** Does the resulting SKOS taxonomy provide correct answers to competency questions when queried with SPARQL?
* **SRQ3:** How can the NIST CSF 2.0 taxonomy be linked to the existing ISO/IEC 27001 SKOS taxonomy to support cross-standard navigation?

## Folder structure

```text
validation/
├── all_cq_sparql_queries.md
├── cq_query_summary.csv
├── nist_csf2_competency_questions.xlsx
├── queries/
├── results/
├── shapes/
├── structural_queries/
├── srq3_mapping_queries/
├── run_cq_queries.py
├── run_structural_checks.py
└── run_srq3_mapping_checks.py
```

## Main files and folders

### `queries/`

Contains the SPARQL queries for the 34 competency questions used for SRQ2. Each `.rq` file corresponds to one competency question. There is also a `check_reference_model.rq` query that checks whether the reference and ISO mapping model is present in the generated taxonomy.

### `structural_queries/`

Contains additional SPARQL checks for structural issues that are easy to inspect in tabular form. These checks include:

* missing English labels,
* duplicate notations,
* reference model counts.

### `srq3_mapping_queries/`

Contains the SPARQL checks used to validate the ISO/IEC 27001 mapping model for SRQ3. These checks test whether ISO mappings exist, whether invalid ISO targets exist, whether mappings are attached to the correct type of concept, and whether navigation works in both directions between NIST CSF and ISO/IEC 27001.

### `shapes/`

Contains the SHACL shapes used to validate the structure of the taxonomy.

### `results/`

Contains generated validation output. This folder is created or updated when the validation scripts are run. It includes CSV result files, summary files, and text reports.

## Requirements

Before running the validation scripts, install the project dependencies from the project root:

```bash
pip install -r requirements.txt
```

The validation scripts use `rdflib` to load the generated Turtle file and execute SPARQL queries. SHACL validation also requires `pyshacl`.

## Build the taxonomy first

Before running validation, make sure the taxonomy has been generated:

```bash
python src/build_project.py
```

This creates the main Turtle file:

```text
output/nist_csf2_taxonomy.ttl
```

The validation scripts use this file as input.

If `src/build_project.py` starts the local browser server, you can stop it with `Ctrl+C` after the build has finished.

## Running SRQ2 competency-question validation

Run the competency-question queries from the project root:

```bash
python validation/run_cq_queries.py \
  --data output/nist_csf2_taxonomy.ttl \
  --queries validation/queries \
  --out validation/results
```

This script loads the generated Turtle taxonomy, runs all `.rq` queries in `validation/queries/`, and writes the results to CSV files.

The main output files are:

```text
validation/results/summary.csv
validation/results/cq01_*.csv
validation/results/cq02_*.csv
...
validation/results/cq34_*.csv
validation/results/check_reference_model.csv
```

The `summary.csv` file shows whether each query executed successfully and how many rows it returned.

A query has status `OK` when it executed without errors. The returned rows should still be compared with the expected answer in the competency-question table.

## Checking the reference model

The query `check_reference_model.rq` is included as a sanity check. After running the SRQ2 queries, open:

```text
validation/results/check_reference_model.csv
```

This file should show that the taxonomy contains:

* `dcterms:references` links from NIST CSF concepts to local Informative Reference concepts,
* local Informative Reference concepts,
* `skos:exactMatch` links from ISO-related reference concepts to Ion's ISO/IEC 27001 taxonomy concepts.

If these counts are missing or zero, rebuild the taxonomy and check that `data/informative_reference_links.csv` and `data/iso-security.ttl` are available.

## Running structural SPARQL checks

Run the structural SPARQL checks from the project root:

```bash
python validation/run_structural_checks.py
```

This script uses:

```text
output/nist_csf2_taxonomy.ttl
validation/structural_queries/
```

It writes the report to:

```text
validation/results/structural_sparql_report.txt
```

The structural SPARQL checks currently test:

* whether all core concepts have English preferred labels,
* whether duplicate notations exist within the same scheme,
* whether the reference model contains references, informative reference concepts, and ISO exact-match links.

The expected result is:

```text
Overall status: PASS
```

## Running SHACL validation

The SHACL shapes are stored in:

```text
validation/shapes/nist_csf_shapes.ttl
```

To run SHACL validation manually from the project root:

```bash
pyshacl \
  -s validation/shapes/nist_csf_shapes.ttl \
  -d output/nist_csf2_taxonomy.ttl \
  -f human \
  > validation/results/shacl_report.txt
```

The expected result is that the report shows:

```text
Conforms: True
```

This means that the generated RDF graph satisfies the structural constraints defined in the SHACL shapes.

## Running SRQ3 ISO/IEC 27001 mapping validation

Run the SRQ3 mapping checks from the project root:

```bash
python validation/run_srq3_mapping_checks.py
```

This script uses:

```text
output/nist_csf2_taxonomy.ttl
validation/srq3_mapping_queries/
```

It writes the results to:

```text
validation/results/srq3_mapping/
```

The main output files are:

```text
validation/results/srq3_mapping/m01_iso_mapping_count.csv
validation/results/srq3_mapping/m02_invalid_iso_targets.csv
validation/results/srq3_mapping/m03_invalid_mapping_subjects.csv
validation/results/srq3_mapping/m04_nist_to_iso_navigation.csv
validation/results/srq3_mapping/m05_iso_to_nist_navigation.csv
validation/results/srq3_mapping/summary.csv
validation/results/srq3_mapping/srq3_mapping_report.txt
```

The SRQ3 checks are:

| Check | Purpose                                                                | Expected result              |
| ----- | ---------------------------------------------------------------------- | ---------------------------- |
| M01   | Check that ISO mappings exist                                          | Mapping count greater than 0 |
| M02   | Check that ISO mapping targets point to Ion's ISO taxonomy namespace   | 0 invalid rows               |
| M03   | Check that mappings start from Informative Reference concepts          | 0 invalid rows               |
| M04   | Check navigation from NIST CSF concepts to ISO/IEC 27001 concepts      | Rows returned                |
| M05   | Check navigation from ISO/IEC 27001 concepts back to NIST CSF concepts | Rows returned                |

The expected final result is:

```text
Overall status: PASS
```

## Recommended validation order

Run the validation in this order:

```bash
python validation/run_structural_checks.py
```

```bash
pyshacl \
  -s validation/shapes/nist_csf_shapes.ttl \
  -d output/nist_csf2_taxonomy.ttl \
  -f human \
  > validation/results/shacl_report.txt
```

```bash
python validation/run_cq_queries.py \
  --data output/nist_csf2_taxonomy.ttl \
  --queries validation/queries \
  --out validation/results
```

```bash
python validation/run_srq3_mapping_checks.py
```

## How to interpret the results

For the structural checks and SRQ3 mapping checks, the scripts automatically evaluate whether each check passes or fails.

For competency questions, the script checks whether each SPARQL query runs and records the number of returned rows. The returned rows should be compared with the expected answers in:

```text
validation/nist_csf2_competency_questions.xlsx
```

The final validation evidence is stored in:

```text
validation/results/
```

## Notes

The validation files are part of the research evidence. Query files should be edited only when the competency questions or taxonomy model change. Result CSV files are generated outputs and should not be edited manually.

