# NIST CSF 2.0 SKOS Taxonomy

This repository contains the implementation for the research project:

**Creating a Machine-Readable SKOS Taxonomy of the NIST Cybersecurity Framework 2.0**

The project converts the NIST Cybersecurity Framework (CSF) 2.0 Core into an RDF/SKOS taxonomy. The generated taxonomy represents NIST CSF Functions, Categories, Subcategories, implementation examples, Informative References, external links, and selected ISO/IEC 27001 mappings.

The repository also includes a local browser for exploring the taxonomy and validation scripts for checking the structure, competency-question results, and ISO/IEC 27001 mapping model.

## Main output

The main generated taxonomy is:

```text
output/nist_csf2_taxonomy.ttl
```

This Turtle file contains the RDF/SKOS representation of the NIST CSF 2.0 Core and the local Informative Reference concepts.

The generated browser is:

```text
website/index.html
```

## Repository structure

```text
.
├── data/
│   ├── csf/
│   │   └── languages/
│   │       ├── csf2_en_english.xlsx
│   │       ├── csf2_de_german.xlsx
│   │       ├── csf2_fr_french.xlsx
│   │       └── ...
│   ├── informative_reference_links.csv
│   ├── iso-security.ttl
│   └── nist_csf2core.csv
├── docs/
│   ├── nist_csf2_taxonomy.ttl
│   └── Research_Proposal_ISO.pdf
├── output/
│   ├── nist_csf2core.csv
│   └── nist_csf2_taxonomy.ttl
├── src/
│   ├── build_project.py
│   └── pipeline/
│       ├── extract_csf_core.py
│       ├── extract_reference.py
│       ├── build_taxonomy.py
│       └── build_browser.py
├── validation/
│   ├── queries/
│   ├── structural_queries/
│   ├── srq3_mapping_queries/
│   ├── shapes/
│   ├── results/
│   ├── run_cq_queries.py
│   ├── run_structural_checks.py
│   ├── run_srq3_mapping_checks.py
│   └── README.md
├── website/
│   └── index.html
├── requirements.txt
└── README.md
```

## Requirements

The project uses Python and RDF/Semantic Web libraries.

Install the required packages from the project root:

```bash
pip install -r requirements.txt
```

A virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Building the project

Run the full build pipeline from the project root:

```bash
python src/build_project.py
```

This script runs the main pipeline steps:

1. Extract the multilingual NIST CSF 2.0 Core into a clean CSV.
2. Build the RDF/SKOS Turtle taxonomy.
3. Generate the local HTML browser.
4. Start a local web server for the browser.

When the build finishes, the browser is served at:

```text
http://localhost:8000
```

Press `Ctrl+C` to stop the local browser server.

## Pipeline scripts

### `src/build_project.py`

Runs the full project pipeline. It creates the output folders, runs the extraction and build scripts, generates the browser, and starts a local HTTP server.

### `src/pipeline/extract_csf_core.py`

Reads the multilingual NIST CSF 2.0 spreadsheet files from:

```text
data/csf/languages/
```

It creates a cleaned CSV file:

```text
output/nist_csf2core.csv
```

The English spreadsheet is used as the structural reference because it contains the most complete structure, implementation examples, and Informative References. Other language files are used to add multilingual labels and descriptions.

### `src/pipeline/extract_reference.py`

Extracts unique Informative References from the cleaned CSF Core CSV.

It creates an unfilled reference-link CSV:

```text
output/informative_reference_links_unfilled.csv
```

This helper script is useful when preparing or updating the Informative Reference link file.

### `src/pipeline/build_taxonomy.py`

Converts the cleaned CSV files into the RDF/SKOS taxonomy.

Input files:

```text
output/nist_csf2core.csv
data/informative_reference_links.csv
data/iso-security.ttl
```

Output file:

```text
output/nist_csf2_taxonomy.ttl
```

The script creates:

* NIST CSF Core concepts,
* local Informative Reference concepts,
* SKOS hierarchy links,
* multilingual labels and definitions,
* implementation examples,
* external reference links,
* selected ISO/IEC 27001 mappings.

### `src/pipeline/build_browser.py`

Generates a static HTML browser from the generated Turtle taxonomy.

Input files:

```text
output/nist_csf2_taxonomy.ttl
data/iso-security.ttl
```

Output file:

```text
website/index.html
```

The browser supports:

* searching concepts,
* browsing the NIST CSF hierarchy,
* viewing labels, definitions, implementation examples, and references,
* switching languages,
* graph exploration,
* navigation between NIST CSF concepts and ISO/IEC 27001 concepts.

## Data files

### `data/csf/languages/`

Contains the NIST CSF 2.0 spreadsheet exports in multiple languages.

### `data/informative_reference_links.csv`

Contains local Informative Reference entries and external links. This file is used when building the taxonomy so that reference concepts can be enriched with external web links.

### `data/iso-security.ttl`

Contains the existing ISO/IEC 27001 SKOS taxonomy used for cross-standard linking.

## Validation

The `validation/` folder contains the validation material for the taxonomy.

It supports:

* structural validation,
* competency-question validation,
* ISO/IEC 27001 mapping validation.

More detailed validation instructions are available in:

```text
validation/README.md
```

## Running structural SPARQL checks

From the project root:

```bash
python validation/run_structural_checks.py
```

This writes:

```text
validation/results/structural_sparql_report.txt
```

These checks test for missing English labels, duplicate notations, and reference model counts.

## Running SHACL validation

From the project root:

```bash
pyshacl \
  -s validation/shapes/nist_csf_shapes.ttl \
  -d output/nist_csf2_taxonomy.ttl \
  -f human \
  > validation/results/shacl_report.txt
```

The expected result is:

```text
Conforms: True
```

## Running competency-question validation

From the project root:

```bash
python validation/run_cq_queries.py \
  --data output/nist_csf2_taxonomy.ttl \
  --queries validation/queries \
  --out validation/results
```

This runs the SPARQL queries for the 34 competency questions and writes one CSV file per query.

The summary file is:

```text
validation/results/summary.csv
```

The competency questions are stored in:

```text
validation/nist_csf2_competency_questions.xlsx
```

## Running ISO/IEC 27001 mapping validation

From the project root:

```bash
python validation/run_srq3_mapping_checks.py
```

This writes results to:

```text
validation/results/srq3_mapping/
```

The main report is:

```text
validation/results/srq3_mapping/srq3_mapping_report.txt
```

The mapping checks test whether:

* ISO mappings exist,
* invalid ISO mapping targets are absent,
* mappings are attached to local Informative Reference concepts,
* navigation works from NIST CSF to ISO/IEC 27001,
* navigation works from ISO/IEC 27001 back to NIST CSF.

## Generated files

The following folders contain generated files:

```text
output/
website/
validation/results/
```

These files can be regenerated by running the build and validation scripts.

## Notes

The repository may contain a local `.venv/` folder when working on the project. This folder is only for the local Python environment and should not be treated as part of the source code.

The `.git/` folder is Git's internal folder and is not part of the project documentation.

## Author

Gheorghe Turca
University of Twente
Student number: s3197999

