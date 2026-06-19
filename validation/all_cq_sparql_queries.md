# SRQ2 competency questions converted to SPARQL

Use these queries to answer: **SRQ2: Does the resulting SKOS taxonomy provide correct answers to competency questions when queried with SPARQL?**

All queries use the NIST CSF 2.0 SKOS model with `skos:broader`, `skos:notation`, `skos:prefLabel`, `skos:definition`, `dcterms:references`, `rdfs:seeAlso`, and `skos:exactMatch`.


## CQ01

**Question:** Which CSF outcomes help an organization understand its mission, stakeholders, dependencies, and legal or contractual requirements?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: GV.OC subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:GV-OC ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ02

**Question:** Which CSF outcomes help define cybersecurity risk objectives, risk appetite, and risk tolerance?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: GV.RM subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:GV-RM ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ03

**Question:** Which CSF outcomes help define who is responsible and accountable for cybersecurity risk management?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: GV.RR subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:GV-RR ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ04

**Question:** Which CSF outcomes help manage cybersecurity risks from suppliers and third parties?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: GV.SC subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:GV-SC ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ05

**Question:** Which CSF outcomes help identify and inventory hardware, software, services, systems, and data?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected asset-management outcomes from ID.AM

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:ID-AM-01 csf:ID-AM-02 csf:ID-AM-03 csf:ID-AM-04 csf:ID-AM-05 csf:ID-AM-07 csf:ID-AM-08 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ06

**Question:** Which CSF outcomes help assess vulnerabilities, threats, likelihood, and impact?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: ID.RA subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:ID-RA ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ07

**Question:** Which CSF outcomes help identify improvements after audits, assessments, incidents, or lessons learned?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: ID.IM subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:ID-IM ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ08

**Question:** Which CSF outcomes help manage identity, authentication, and access control?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: PR.AA subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:PR-AA ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ09

**Question:** Which CSF outcomes help protect employees and users through cybersecurity awareness and training?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: PR.AT subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:PR-AT ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ10

**Question:** Which CSF outcomes help protect data confidentiality, integrity, and availability?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected data-security outcomes from PR.DS

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:PR-DS-01 csf:PR-DS-02 csf:PR-DS-10 csf:PR-DS-11 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ11

**Question:** Which CSF outcomes help protect systems through secure configuration, patching, backups, logging, and infrastructure resilience?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected platform-security and infrastructure-resilience outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:PR-PS csf:PR-PS-01 csf:PR-PS-02 csf:PR-PS-03 csf:PR-PS-04 csf:PR-PS-05 csf:PR-PS-06 csf:PR-IR csf:PR-IR-01 csf:PR-IR-02 csf:PR-IR-03 csf:PR-IR-04 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ12

**Question:** Which CSF outcomes help detect cybersecurity attacks, anomalies, and suspicious activity?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected continuous monitoring outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:DE-CM-01 csf:DE-CM-02 csf:DE-CM-03 csf:DE-CM-06 csf:DE-CM-09 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ13

**Question:** Which CSF outcomes help manage and execute incident response activities?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Category traversal: RS.MA subcategories

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  ?concept skos:broader csf:RS-MA ;
           skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ14

**Question:** Which CSF outcomes help communicate and report cybersecurity incidents?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected incident communication outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:RS-CO-02 csf:RS-CO-03 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ15

**Question:** Which CSF outcomes help contain, eradicate, or mitigate cybersecurity incidents?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected incident mitigation outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:RS-MI-01 csf:RS-MI-02 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ16

**Question:** Which CSF outcomes help communicate recovery status after an incident?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected recovery communication outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:RC-CO-03 csf:RC-CO-04 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ17

**Question:** Which NIST CSF Function covers establishing cybersecurity policy and oversight over cybersecurity risk management?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Function and category retrieval for GOVERN, Policy, and Oversight

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?functionNotation ?functionLabel ?functionDefinition ?categoryNotation ?categoryLabel ?categoryDefinition
WHERE {
  csf:GV skos:notation ?functionNotation ;
         skos:prefLabel ?functionLabel ;
         skos:definition ?functionDefinition .
  FILTER(LANGMATCHES(LANG(?functionLabel), "en"))
  FILTER(LANGMATCHES(LANG(?functionDefinition), "en"))

  VALUES ?category { csf:GV-PO csf:GV-OV }
  ?category skos:broader csf:GV ;
            skos:notation ?categoryNotation ;
            skos:prefLabel ?categoryLabel ;
            skos:definition ?categoryDefinition .
  FILTER(LANGMATCHES(LANG(?categoryLabel), "en"))
  FILTER(LANGMATCHES(LANG(?categoryDefinition), "en"))
}
ORDER BY ?categoryNotation
```


## CQ18

**Question:** What is the definition of the NIST CSF GV.OV Oversight Category?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Single category definition retrieval

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  csf:GV-OV skos:notation ?notation ;
            skos:prefLabel ?label ;
            skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
```


## CQ19

**Question:** What is the definition of the NIST CSF ID.RA-08 Subcategory?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Single subcategory definition retrieval

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  csf:ID-RA-08 skos:notation ?notation ;
            skos:prefLabel ?label ;
            skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
```


## CQ20

**Question:** Which NIST CSF Category does RS.AN-06 belong to, and what is its definition?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Upward hierarchy navigation and definition retrieval

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?subcategoryNotation ?subcategoryLabel ?subcategoryDefinition ?categoryNotation ?categoryLabel ?categoryDefinition
WHERE {
  csf:RS-AN-06 skos:notation ?subcategoryNotation ;
              skos:prefLabel ?subcategoryLabel ;
              skos:definition ?subcategoryDefinition ;
              skos:broader ?category .
  ?category skos:notation ?categoryNotation ;
            skos:prefLabel ?categoryLabel ;
            skos:definition ?categoryDefinition .
  FILTER(LANGMATCHES(LANG(?subcategoryLabel), "en"))
  FILTER(LANGMATCHES(LANG(?subcategoryDefinition), "en"))
  FILTER(LANGMATCHES(LANG(?categoryLabel), "en"))
  FILTER(LANGMATCHES(LANG(?categoryDefinition), "en"))
}
```


## CQ21

**Question:** Which NIST CSF outcomes and references are relevant when responding to a leaked accounts database containing user account information?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Scenario outcome retrieval with informative references

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition ?referenceNotation ?referenceLabel ?referenceURL ?isoConcept
WHERE {
  VALUES ?concept { csf:ID-AM-07 csf:ID-RA-04 csf:DE-AE-04 csf:DE-AE-08 csf:RS-AN-03 csf:RS-AN-07 csf:RS-CO-02 csf:RS-MI-01 csf:RC-RP-02 csf:ID-IM-04 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))

  OPTIONAL { ?reference rdfs:seeAlso ?referenceURL . }
  OPTIONAL { ?reference skos:exactMatch ?isoConcept . }
}
ORDER BY ?notation ?referenceNotation
```


## CQ22

**Question:** Which NIST CSF outcomes and references are relevant when employee credentials are suspected to be compromised?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Scenario outcome retrieval with informative references

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition ?referenceNotation ?referenceLabel ?referenceURL ?isoConcept
WHERE {
  VALUES ?concept { csf:PR-AA-01 csf:PR-AA-03 csf:PR-AA-05 csf:DE-CM-03 csf:DE-AE-02 csf:RS-AN-03 csf:RS-MI-01 csf:RS-CO-02 csf:ID-IM-04 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))

  OPTIONAL { ?reference rdfs:seeAlso ?referenceURL . }
  OPTIONAL { ?reference skos:exactMatch ?isoConcept . }
}
ORDER BY ?notation ?referenceNotation
```


## CQ23

**Question:** Which NIST CSF outcomes and references are relevant when ransomware affects critical business systems?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Scenario outcome retrieval with informative references

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition ?referenceNotation ?referenceLabel ?referenceURL ?isoConcept
WHERE {
  VALUES ?concept { csf:ID-AM-05 csf:PR-DS-11 csf:PR-PS-01 csf:PR-PS-04 csf:PR-IR-03 csf:DE-CM-09 csf:RS-MA-01 csf:RS-MI-01 csf:RS-MI-02 csf:RC-RP-01 csf:RC-RP-03 csf:RC-CO-03 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))

  OPTIONAL { ?reference rdfs:seeAlso ?referenceURL . }
  OPTIONAL { ?reference skos:exactMatch ?isoConcept . }
}
ORDER BY ?notation ?referenceNotation
```


## CQ24

**Question:** Which NIST CSF outcomes and references are relevant when a third-party supplier suffers a security breach?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Scenario outcome retrieval with informative references

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition ?referenceNotation ?referenceLabel ?referenceURL ?isoConcept
WHERE {
  VALUES ?concept { csf:GV-SC-04 csf:GV-SC-07 csf:GV-SC-08 csf:GV-OC-05 csf:ID-RA-10 csf:DE-AE-04 csf:RS-CO-02 csf:RS-MI-01 csf:ID-IM-02 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))

  OPTIONAL { ?reference rdfs:seeAlso ?referenceURL . }
  OPTIONAL { ?reference skos:exactMatch ?isoConcept . }
}
ORDER BY ?notation ?referenceNotation
```


## CQ25

**Question:** Which NIST CSF Subcategories are relevant when an organization discovers unpatched internet-facing systems?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Scenario outcome retrieval by selected notations

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:ID-AM-01 csf:ID-AM-02 csf:ID-RA-01 csf:ID-RA-05 csf:ID-RA-06 csf:PR-PS-02 csf:DE-CM-09 csf:RS-MI-01 csf:ID-IM-03 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ26

**Question:** Which NIST CSF Subcategories are relevant when a cloud storage bucket containing sensitive data is accidentally exposed to the internet?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Scenario outcome retrieval by selected notations

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:ID-AM-04 csf:ID-AM-07 csf:PR-DS-01 csf:PR-DS-02 csf:PR-AA-05 csf:DE-CM-09 csf:DE-AE-04 csf:DE-AE-08 csf:RS-MI-01 csf:RS-CO-02 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ27

**Question:** Which ISO/IEC 27001 controls are related to NIST CSF access-control outcomes?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Cross-standard tracing from PR.AA outcomes to ISO taxonomy through dcterms:references and skos:exactMatch

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?nistNotation ?nistLabel ?referenceNotation ?referenceLabel ?referenceURL ?isoConcept ?isoLabel
WHERE {
  VALUES ?concept { csf:PR-AA-01 csf:PR-AA-02 csf:PR-AA-03 csf:PR-AA-04 csf:PR-AA-05 csf:PR-AA-06 }
  ?concept skos:notation ?nistNotation ;
           skos:prefLabel ?nistLabel ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?nistLabel), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel ;
             skos:exactMatch ?isoConcept .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))
  FILTER(STRSTARTS(STR(?isoConcept), "https://wiren301.github.io/iso27001-skos-taxonomy/"))

  OPTIONAL { ?reference rdfs:seeAlso ?referenceURL . }
  OPTIONAL {
    ?isoConcept skos:prefLabel ?isoLabel .
    FILTER(LANG(?isoLabel) = "" || LANGMATCHES(LANG(?isoLabel), "en"))
  }
}
ORDER BY ?nistNotation ?referenceNotation
```


## CQ28

**Question:** Which ISO/IEC 27001 controls are linked to the NIST CSF PR.PS-04 Subcategory for log records and continuous monitoring?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Cross-standard tracing from PR.PS-04 to ISO taxonomy

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?nistNotation ?nistLabel ?referenceNotation ?referenceLabel ?referenceURL ?isoConcept ?isoLabel
WHERE {
  VALUES ?concept { csf:PR-PS-04 }
  ?concept skos:notation ?nistNotation ;
           skos:prefLabel ?nistLabel ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?nistLabel), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel ;
             skos:exactMatch ?isoConcept .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))
  FILTER(STRSTARTS(STR(?isoConcept), "https://wiren301.github.io/iso27001-skos-taxonomy/"))

  OPTIONAL { ?reference rdfs:seeAlso ?referenceURL . }
  OPTIONAL {
    ?isoConcept skos:prefLabel ?isoLabel .
    FILTER(LANG(?isoLabel) = "" || LANGMATCHES(LANG(?isoLabel), "en"))
  }
}
ORDER BY ?nistNotation ?referenceNotation
```


## CQ29

**Question:** Which NIST CSF Subcategories are linked to ISO/IEC 27001 control A.8.13 Information backup?

**Expected result type:** NIST concept(s), informative reference concept(s), external URL(s), and ISO exactMatch URI(s)

**Validates:** Reverse cross-standard tracing from ISO A.8.13 to NIST concepts

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition ?referenceNotation ?referenceLabel ?isoConcept ?isoLabel
WHERE {
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition ;
           dcterms:references ?reference .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))

  ?reference skos:notation ?referenceNotation ;
             skos:prefLabel ?referenceLabel ;
             skos:exactMatch <https://wiren301.github.io/iso27001-skos-taxonomy/27001/control/A.8.13> .
  FILTER(LANGMATCHES(LANG(?referenceLabel), "en"))

  BIND(<https://wiren301.github.io/iso27001-skos-taxonomy/27001/control/A.8.13> AS ?isoConcept)

  OPTIONAL {
    ?isoConcept skos:prefLabel ?isoLabel .
    FILTER(LANG(?isoLabel) = "" || LANGMATCHES(LANG(?isoLabel), "en"))
  }
}
ORDER BY ?notation
```


## CQ30

**Question:** Who is responsible for cybersecurity risk management and supplier security responsibilities?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected responsibility/accountability outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:GV-RR-01 csf:GV-RR-02 csf:GV-SC-02 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ31

**Question:** How can user accounts and credentials be protected against unauthorized access?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected identity, credential, access, and monitoring outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:PR-AA-01 csf:PR-AA-02 csf:PR-AA-03 csf:PR-AA-04 csf:PR-AA-05 csf:DE-CM-03 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ32

**Question:** Which CSF outcomes help ensure backups are available and safe to use after an incident?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected backup and restoration outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:PR-DS-11 csf:RC-RP-03 csf:RC-RP-05 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ33

**Question:** Which CSF outcomes help monitor supplier or external service provider cybersecurity activities?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected supplier-monitoring outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:GV-SC-07 csf:GV-SC-09 csf:DE-CM-06 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```


## CQ34

**Question:** Which CSF subcategories help decide whether an adverse event should become a declared incident and be escalated?

**Expected result type:** CSF notation(s), English label(s), and English definition(s)

**Validates:** Selected incident declaration, triage, prioritization, and escalation outcomes

```sparql
PREFIX csf: <https://w3id.org/nist-csf2-skos/concept/>
PREFIX csfref: <https://w3id.org/nist-csf2-skos/reference/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?notation ?label ?definition
WHERE {
  VALUES ?concept { csf:DE-AE-08 csf:RS-MA-02 csf:RS-MA-03 csf:RS-MA-04 }
  ?concept skos:notation ?notation ;
           skos:prefLabel ?label ;
           skos:definition ?definition .
  FILTER(LANGMATCHES(LANG(?label), "en"))
  FILTER(LANGMATCHES(LANG(?definition), "en"))
}
ORDER BY ?notation
```
