# Code by georgeturca
# Build a local browser for navigating linked NIST CSF 2.0 and ISO/IEC 27001 SKOS taxonomies.

from pathlib import Path
import json

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, SKOS, DCTERMS, RDFS


NIST_FILE = Path("output/nist_csf2_taxonomy.ttl")
ISO_FILE = Path("data/iso-security.ttl")
OUTPUT_FILE = Path("website/index.html")

NIST_CORE_SCHEME = "https://w3id.org/nist-csf2-skos/scheme/core"


def literal_values(graph, subject, predicate):
    values = []

    for value in graph.objects(subject, predicate):
        if isinstance(value, Literal):
            values.append({
                "value": str(value),
                "lang": value.language or "",
            })

    return values


def uri_values(graph, subject, predicate):
    return [
        str(value)
        for value in graph.objects(subject, predicate)
        if isinstance(value, URIRef)
    ]


def pick_literal(values):
    if not values:
        return ""

    for item in values:
        if item["lang"] == "en":
            return item["value"]

    for item in values:
        if item["lang"] == "":
            return item["value"]

    return values[0]["value"]


def short_uri(uri):
    replacements = {
        "https://w3id.org/nist-csf2-skos/concept/": "csf:",
        "https://w3id.org/nist-csf2-skos/reference/": "csfref:",
        "https://wiren301.github.io/iso27001-skos-taxonomy/27001/clause/": "iso27001-clause:",
        "https://wiren301.github.io/iso27001-skos-taxonomy/27001/control/": "iso27001-control:",
        "https://wiren301.github.io/iso27001-skos-taxonomy/27002/control/": "iso27002-control:",
        "https://wiren301.github.io/iso27001-skos-taxonomy/27000/term/": "iso27000-term:",
    }

    for full, prefix in replacements.items():
        if uri.startswith(full):
            return prefix + uri.replace(full, "")

    return uri


def vocabulary_name(uri):
    if uri.startswith("https://w3id.org/nist-csf2-skos/concept/"):
        return "NIST CSF Core"

    if uri.startswith("https://w3id.org/nist-csf2-skos/reference/"):
        return "NIST Informative References"

    if "iso27001-skos-taxonomy/27001/clause/" in uri:
        return "ISO 27001 Requirements"

    if "iso27001-skos-taxonomy/27001/control/" in uri:
        return "ISO 27001 Annex A"

    if "iso27001-skos-taxonomy/27002/control/" in uri:
        return "ISO 27002 Controls"

    if "iso27001-skos-taxonomy/27000/term/" in uri:
        return "ISO 27000 Vocabulary"

    if "iso27001-skos-taxonomy" in uri:
        return "ISO Taxonomy"

    return "Other"


def fallback_label(uri, notation):
    if notation:
        return notation

    return uri.rstrip("/").split("/")[-1]


def main():
    if not NIST_FILE.exists():
        raise FileNotFoundError(f"Could not find NIST TTL: {NIST_FILE}")

    graph = Graph()
    graph.parse(NIST_FILE, format="turtle")

    if ISO_FILE.exists():
        graph.parse(ISO_FILE, format="turtle")
    else:
        print(f"Warning: ISO TTL not found: {ISO_FILE}")
        print("The browser will still work, but ISO exactMatch targets may open as external links.")

    concepts = {}
    languages = {"en"}

    for concept in graph.subjects(RDF.type, SKOS.Concept):
        uri = str(concept)

        labels = literal_values(graph, concept, SKOS.prefLabel)
        definitions = literal_values(graph, concept, SKOS.definition)
        examples = literal_values(graph, concept, SKOS.example)
        notations = literal_values(graph, concept, SKOS.notation)
        types = literal_values(graph, concept, DCTERMS.type)

        for item in labels + definitions + examples:
            if item["lang"]:
                languages.add(item["lang"])

        notation = pick_literal(notations)
        label = pick_literal(labels)

        if not label:
            label = fallback_label(uri, notation)

        concepts[uri] = {
            "uri": uri,
            "shortUri": short_uri(uri),
            "vocabulary": vocabulary_name(uri),
            "label": label,
            "labels": labels,
            "definition": pick_literal(definitions),
            "definitions": definitions,
            "examples": examples,
            "notation": notation,
            "types": [item["value"] for item in types],
            "inScheme": uri_values(graph, concept, SKOS.inScheme),
            "broader": uri_values(graph, concept, SKOS.broader),
            "narrower": uri_values(graph, concept, SKOS.narrower),
            "related": uri_values(graph, concept, SKOS.related),
            "references": uri_values(graph, concept,DCTERMS.references),
            "exactMatch": uri_values(graph, concept, SKOS.exactMatch),
            "seeAlso": uri_values(graph, concept, RDFS.seeAlso),
            "referencedBy": [],
            "matchedBy": [],
        }

    # Reverse links: ISO concept -> NIST reference concepts that exactMatch it.
    for subject, _, obj in graph.triples((None, SKOS.exactMatch, None)):
        subject_uri = str(subject)
        object_uri = str(obj)

        if object_uri in concepts and subject_uri in concepts:
            concepts[object_uri]["matchedBy"].append(subject_uri)
    
    # Reverse links: informative reference concept -> NIST concepts that reference it.
    for subject, _, obj in graph.triples((None, DCTERMS.references, None)):
        subject_uri = str(subject)
        object_uri = str(obj)

        if object_uri in concepts and subject_uri in concepts:
            concepts[object_uri]["referencedBy"].append(subject_uri)

    nist_roots = [
        str(concept)
        for concept in graph.objects(URIRef(NIST_CORE_SCHEME), SKOS.hasTopConcept)
        if str(concept) in concepts
    ]

    if not nist_roots:
        for uri, concept in concepts.items():
            if NIST_CORE_SCHEME in concept["inScheme"] and not concept["broader"]:
                nist_roots.append(uri)

    nist_roots.sort(key=lambda uri: concepts[uri]["notation"] or concepts[uri]["label"])

    data = {
        "concepts": concepts,
        "nistRoots": nist_roots,
        "vocabularies": sorted(set(concept["vocabulary"] for concept in concepts.values())),
        "languages": sorted(languages),
    }

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NIST CSF 2.0 and ISO 27001 Linked Taxonomy Browser</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f6f8;
            color: #222;
        }}

        header {{
            background: #1f2937;
            color: white;
            padding: 12px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
        }}

        header h1 {{
            margin: 0;
            font-size: 20px;
            white-space: nowrap;
        }}

        .top-controls {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .top-controls label {{
            font-size: 12px;
            color: #d1d5db;
        }}

        .top-controls select,
        .top-controls button,
        .top-controls a.nav-button {{
            width: auto;
            margin: 0;
            padding: 7px 9px;
            border: 1px solid #4b5563;
            border-radius: 6px;
            background: white;
            color: #111827;
            font-size: 13px;
        }}

        .top-controls button,
        .top-controls a.nav-button {{
            cursor: pointer;
        }}

        .top-controls a.nav-button {{
            display: inline-block;
            text-decoration: none;
        }}

        .top-controls a.nav-button:hover,
        .top-controls button:hover {{
            background: #e5e7eb;
            text-decoration: none;
        }}

        .modal-backdrop {{
            position: fixed;
            inset: 0;
            background: rgba(17, 24, 39, 0.65);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            z-index: 1000;
        }}

        .modal-content {{
            width: min(720px, 100%);
            max-height: 90vh;
            overflow-y: auto;
            background: white;
            color: #111827;
            border-radius: 10px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
            padding: 24px;
            position: relative;
            line-height: 1.5;
        }}

        .modal-content h2 {{
            margin-top: 0;
            margin-right: 34px;
        }}

        .modal-content h3 {{
            margin-bottom: 6px;
        }}

        .modal-close {{
            position: absolute;
            top: 14px;
            right: 14px;
            border: none;
            background: #f3f4f6;
            color: #111827;
            border-radius: 999px;
            width: 32px;
            height: 32px;
            cursor: pointer;
            font-size: 18px;
            line-height: 1;
        }}

        .modal-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 18px;
        }}

        .modal-actions a {{
            display: inline-block;
            padding: 9px 12px;
            border-radius: 6px;
            background: #1f2937;
            color: white;
            text-decoration: none;
        }}

        .modal-actions a.secondary {{
            background: #e5e7eb;
            color: #111827;
        }}

        .layout {{
            display: grid;
            grid-template-columns: 38% 62%;
            height: calc(100vh - 58px);
        }}

        aside {{
            background: white;
            border-right: 1px solid #ddd;
            overflow-y: auto;
            padding: 16px;
        }}

        main {{
            overflow-y: auto;
            padding: 24px;
        }}

        input, select {{
            width: 100%;
            box-sizing: border-box;
            padding: 10px;
            margin-bottom: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }}

        .tree ul {{
            list-style: none;
            padding-left: 20px;
        }}

        .tree li {{
            margin: 4px 0;
        }}

        .tree-row {{
            display: flex;
            align-items: flex-start;
            gap: 4px;
        }}

        .expander {{
            border: none;
            background: none;
            cursor: pointer;
            width: 22px;
            padding: 3px 0;
            color: #333;
            font-size: 13px;
        }}

        .expander-placeholder {{
            display: inline-block;
            width: 22px;
        }}

        .node, .concept-link {{
            border: none;
            background: none;
            color: #0645ad;
            cursor: pointer;
            text-align: left;
            padding: 3px 4px;
            border-radius: 4px;
            font-size: 14px;
        }}

        .node:hover, .concept-link:hover {{
            background: #e5e7eb;
            text-decoration: underline;
        }}

        .selected {{
            background: #dbeafe;
            font-weight: bold;
        }}

        .card {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 18px;
        }}

        .card h2 {{
            margin-top: 0;
        }}

        .graph-card {{
            height: calc(100vh - 116px);
            display: flex;
            flex-direction: column;
            padding: 0;
            overflow: hidden;
        }}

        .graph-title {{
            padding: 14px 18px;
            border-bottom: 1px solid #ddd;
            background: white;
        }}

        .graph-title h2 {{
            margin: 0;
            font-size: 18px;
        }}

        .graph-title p {{
            margin: 4px 0 0 0;
            font-size: 12px;
            color: #666;
        }}

        .meta {{
            color: #555;
            font-size: 14px;
            line-height: 1.5;
        }}

        .badge {{
            display: inline-block;
            background: #e5e7eb;
            border-radius: 999px;
            padding: 2px 8px;
            font-size: 12px;
            margin-left: 5px;
            color: #333;
        }}

        ul {{
            margin-top: 8px;
        }}

        li {{
            margin-bottom: 6px;
        }}

        a {{
            color: #0645ad;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .small {{
            color: #666;
            font-size: 12px;
        }}

        .uri {{
            word-break: break-all;
            font-family: monospace;
            background: #f3f4f6;
            padding: 4px 6px;
            border-radius: 4px;
        }}

        .hidden {{
            display: none !important;
        }}

        .graph-box {{
            flex: 1;
            min-height: 420px;
            background: #f9fafb;
            border-top: 1px solid #e5e7eb;
            position: relative;
            overflow: hidden;
        }}

        .graph-svg {{
            width: 100%;
            height: 100%;
            cursor: grab;
            user-select: none;
            touch-action: none;
        }}

        .graph-svg.dragging {{
            cursor: grabbing;
        }}

        .graph-edge {{
            stroke: #9ca3af;
            stroke-width: 1.4;
        }}

        .graph-edge.hierarchy {{
            stroke: #2563eb;
        }}

        .graph-edge.reference {{
            stroke: #7c3aed;
        }}

        .graph-edge.match {{
            stroke: #059669;
        }}

        .graph-edge.related {{
            stroke: #d97706;
        }}

        .graph-node {{
            cursor: pointer;
        }}

        .graph-node circle {{
            fill: white;
            stroke: #2563eb;
            stroke-width: 2;
        }}

        .graph-node.root circle {{
            stroke: #111827;
            stroke-width: 3;
            fill: #fef3c7;
        }}

        .graph-node.reference circle {{
            stroke: #7c3aed;
            fill: #f5f3ff;
        }}

        .graph-node.iso circle {{
            stroke: #059669;
            fill: #ecfdf5;
        }}

        .graph-node.nist circle {{
            stroke: #2563eb;
            fill: #eff6ff;
        }}

        .graph-node text {{
            font-size: 11px;
            fill: #111827;
            pointer-events: none;
        }}

        .graph-edge-label {{
            font-size: 10px;
            fill: #6b7280;
            pointer-events: none;
            paint-order: stroke;
            stroke: #f9fafb;
            stroke-width: 3px;
        }}

        .legend {{
            position: absolute;
            right: 12px;
            bottom: 12px;
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
            line-height: 1.7;
        }}

        .legend span {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 6px;
            vertical-align: middle;
        }}

        .legend .nist-dot {{ background: #eff6ff; border: 2px solid #2563eb; }}
        .legend .ref-dot {{ background: #f5f3ff; border: 2px solid #7c3aed; }}
        .legend .iso-dot {{ background: #ecfdf5; border: 2px solid #059669; }}

        @media (max-width: 1000px) {{
            header {{
                align-items: flex-start;
                flex-direction: column;
            }}

            header h1 {{
                white-space: normal;
            }}

            .layout {{
                grid-template-columns: 1fr;
                height: auto;
            }}

            aside {{
                border-right: none;
                border-bottom: 1px solid #ddd;
                max-height: 45vh;
            }}
        }}
    </style>
</head>
<body>
<header>
    <h1>NIST CSF 2.0 and ISO 27001 Linked Taxonomy Browser</h1>

    <div class="top-controls">
        <label for="languageSelect">Language</label>
        <select id="languageSelect" onchange="setLanguage(this.value)"></select>

        <label for="viewMode">View</label>
        <select id="viewMode" onchange="setViewMode(this.value)">
            <option value="info">Information</option>
            <option value="graph">Graph</option>
        </select>

        <button type="button" onclick="openThesisInfo()">About thesis</button>
        <a class="nav-button" href="https://github.com/georgeturca/nistcsf2.0-skos-taxonomy" target="_blank" rel="noopener noreferrer">GitHub repo</a>

        <span id="graphTopControls" class="top-controls hidden">
            <label for="graphType">Graph</label>
            <select id="graphType" onchange="renderDetails()">
                <option value="combined">Combined</option>
                <option value="hierarchy">Hierarchy</option>
                <option value="references">Reference network</option>
                <option value="matches">Exact matches</option>
            </select>

            <label for="graphDepth">Depth</label>
            <select id="graphDepth" onchange="renderDetails()">
                <option value="1">1</option>
                <option value="2" selected>2</option>
                <option value="3">3</option>
                <option value="4">4</option>
            </select>

            <button type="button" onclick="expandGraphDepth()">Expand</button>
            <button type="button" onclick="zoomGraph(1.2)">Zoom +</button>
            <button type="button" onclick="zoomGraph(0.8)">Zoom -</button>
            <button type="button" onclick="resetGraphZoom()">Reset</button>
        </span>
    </div>
</header>

<div id="thesisInfoModal" class="modal-backdrop hidden" onclick="handleModalBackdropClick(event)">
    <div class="modal-content" role="dialog" aria-modal="true" aria-labelledby="thesisInfoTitle">
        <button class="modal-close" type="button" onclick="closeThesisInfo()" aria-label="Close thesis information">×</button>
        <h2 id="thesisInfoTitle">About this thesis</h2>
        <p><strong>Creating a Machine-Readable SKOS Taxonomy of the NIST Cybersecurity Framework 2.0</strong></p>
        <p>This browser is a supporting artifact for exploring the generated NIST CSF 2.0 SKOS taxonomy and its links to the existing ISO/IEC 27001 SKOS taxonomy.</p>
        <h3>What the browser shows</h3>
        <ul>
            <li>NIST CSF 2.0 Functions, Categories, and Subcategories</li>
            <li>labels, definitions, implementation examples, and Informative References</li>
            <li>links from NIST CSF concepts to related ISO/IEC 27001 concepts</li>
            <li>information and graph views for exploring the taxonomy</li>
        </ul>
        <h3>Repository</h3>
        <p>The source code, generated taxonomy files, validation queries, validation results, and browser implementation are available on GitHub.</p>
        <div class="modal-actions">
            <a href="https://github.com/georgeturca/nistcsf2.0-skos-taxonomy" target="_blank" rel="noopener noreferrer">Open GitHub repository</a>
            <a class="secondary" href="https://w3id.org/nist-csf2-skos/" target="_blank" rel="noopener noreferrer">Open W3ID namespace</a>
        </div>
    </div>
</div>

<div class="layout">
    <aside>
        <input id="search" placeholder="Search: GV.OC-01, PR.AA-05, A.8.3, ISO..." oninput="renderSidebar()">

        <select id="vocabFilter" onchange="renderSidebar()">
            <option value="NIST CSF Core">NIST CSF Core</option>
            <option value="NIST Informative References">NIST Informative References</option>
            <option value="ISO 27001 Requirements">ISO 27001 Requirements</option>
            <option value="ISO 27001 Annex A">ISO 27001 Annex A</option>
            <option value="ISO 27002 Controls">ISO 27002 Controls</option>
            <option value="ISO 27000 Vocabulary">ISO 27000 Vocabulary</option>
            <option value="all">All vocabularies</option>
        </select>

        <div id="sidebar" class="tree"></div>
    </aside>

    <main>
        <div id="details" class="card">
            <h2>Select a concept</h2>
            <p>Use the tree or search box on the left.</p>
        </div>
    </main>
</div>

<script>
const DATA = __DATA__;
const concepts = DATA.concepts;
const expandedUris = new Set();
let currentLanguage = "en";
let currentViewMode = "info";
let graphTransform = { x: 0, y: 0, scale: 1 };
let graphDrag = null;

function openThesisInfo() {{
    document.getElementById("thesisInfoModal").classList.remove("hidden");
}}

function closeThesisInfo() {{
    document.getElementById("thesisInfoModal").classList.add("hidden");
}}

function handleModalBackdropClick(event) {{
    if (event.target.id === "thesisInfoModal") {{
        closeThesisInfo();
    }}
}}

document.addEventListener("keydown", function(event) {{
    if (event.key === "Escape") {{
        closeThesisInfo();
    }}
}});

function escapeHtml(value) {{
    return String(value || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}}

function populateLanguageSelect() {{
    const select = document.getElementById("languageSelect");
    const languages = DATA.languages || ["en"];

    select.innerHTML = languages.map(lang => `
        <option value="${{escapeHtml(lang)}}" ${{lang === currentLanguage ? "selected" : ""}}>
            ${{escapeHtml(lang || "none")}}
        </option>
    `).join("");
}}

function setLanguage(language) {{
    currentLanguage = language;
    renderSidebar();
    renderDetails();
}}

function setViewMode(mode) {{
    currentViewMode = mode;
    document.getElementById("graphTopControls").classList.toggle("hidden", mode !== "graph");
    renderDetails();
}}

function expandGraphDepth() {{
    const select = document.getElementById("graphDepth");
    select.value = String(Math.min(4, Number(select.value || 1) + 1));
    renderDetails();
}}

function getLiteral(values) {{
    if (!values || values.length === 0) return "";

    for (const item of values) {{
        if (item.lang === currentLanguage) return item.value;
    }}

    for (const item of values) {{
        if (item.lang === "en") return item.value;
    }}

    for (const item of values) {{
        if (item.lang === "") return item.value;
    }}

    return values[0].value;
}}

function getLiteralList(values) {{
    if (!values || values.length === 0) return [];

    const selected = values.filter(item => item.lang === currentLanguage);
    if (selected.length > 0) return selected;

    const english = values.filter(item => item.lang === "en");
    if (english.length > 0) return english;

    const neutral = values.filter(item => item.lang === "");
    if (neutral.length > 0) return neutral;

    return values;
}}

function navigateTo(uri) {{
    window.location.hash = encodeURIComponent(uri);
}}

function toggleExpand(uri) {{
    if (expandedUris.has(uri)) {{
        expandedUris.delete(uri);
    }} else {{
        expandedUris.add(uri);
    }}

    renderSidebar();
}}

document.addEventListener("click", function(event) {{
    const toggleTarget = event.target.closest("[data-toggle-uri]");

    if (toggleTarget) {{
        toggleExpand(toggleTarget.dataset.toggleUri);
        return;
    }}

    const graphNode = event.target.closest("[data-graph-uri]");

    if (graphNode) {{
        navigateTo(graphNode.dataset.graphUri);
        return;
    }}

    const target = event.target.closest("[data-uri]");

    if (!target) return;

    navigateTo(target.dataset.uri);
}});

window.addEventListener("hashchange", renderDetails);

function getCurrentUri() {{
    if (!window.location.hash) return "";
    return decodeURIComponent(window.location.hash.slice(1));
}}

function displayName(uri) {
    const concept = concepts[uri];

    if (!concept) return uri;

    const notation = (concept.notation || "").trim();
    const label = (concept.label || "").trim();

    if (notation && label && notation.toLowerCase() === label.toLowerCase()) {
        return notation;
    }

    if (notation && label) {
        return notation + " — " + label;
    }

    if (label) {
        return label;
    }

    if (notation) {
        return notation;
    }

    return uri;
}

function conceptButton(uri) {{
    const concept = concepts[uri];

    if (!concept) {{
        return `<a href="${{escapeHtml(uri)}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(uri)}}</a>`;
    }}

    return `
        <button class="concept-link" data-uri="${{escapeHtml(uri)}}">
            ${{escapeHtml(displayName(uri))}}
            <span class="badge">${{escapeHtml(concept.vocabulary)}}</span>
        </button>
    `;
}}

function conceptMatches(concept, query, filter) {{
    if (filter !== "all" && concept.vocabulary !== filter) {{
        return false;
    }}

    if (!query) return true;

    const allLabels = (concept.labels || []).map(item => item.value).join(" ");
    const allDefinitions = (concept.definitions || []).map(item => item.value).join(" ");

    const text = [
        concept.uri,
        concept.shortUri,
        concept.vocabulary,
        allLabels,
        allDefinitions,
        concept.label,
        concept.notation,
        concept.definition,
        concept.types.join(" ")
    ].join(" ").toLowerCase();

    return text.includes(query.toLowerCase());
}}

function subtreeMatches(uri, query) {{
    const concept = concepts[uri];

    if (!concept) return false;

    if (!query) return true;

    if (conceptMatches(concept, query, "all")) return true;

    return concept.narrower.some(childUri => subtreeMatches(childUri, query));
}}

function renderTreeNode(uri, query, depth = 0, visited = new Set()) {{
    if (visited.has(uri)) return "";
    visited.add(uri);

    const concept = concepts[uri];

    if (!concept) return "";

    if (!subtreeMatches(uri, query)) return "";

    const currentUri = getCurrentUri();
    const selectedClass = currentUri === uri ? "selected" : "";

    const children = concept.narrower
        .filter(childUri => concepts[childUri])
        .sort((a, b) => displayName(a).localeCompare(displayName(b)));

    const hasChildren = children.length > 0;
    const isExpanded = query || expandedUris.has(uri);
    const arrow = isExpanded ? "▾" : "▸";

    let html = `
        <li>
            <div class="tree-row">
    `;

    if (hasChildren) {{
        html += `
            <button class="expander" data-toggle-uri="${{escapeHtml(uri)}}" title="Expand/collapse">
                ${{arrow}}
            </button>
        `;
    }} else {{
        html += `<span class="expander-placeholder"></span>`;
    }}

    html += `
            <button class="node ${{selectedClass}}" data-uri="${{escapeHtml(uri)}}">
                ${{escapeHtml(displayName(uri))}}
                <span class="badge">${{escapeHtml(concept.types[0] || concept.vocabulary)}}</span>
            </button>
        </div>
    `;

    if (hasChildren && isExpanded) {{
        html += "<ul>";

        for (const childUri of children) {{
            html += renderTreeNode(childUri, query, depth + 1, new Set(visited));
        }}

        html += "</ul>";
    }}

    html += "</li>";

    return html;
}}

function renderSidebar() {{
    const query = document.getElementById("search").value.trim();
    const filter = document.getElementById("vocabFilter").value;
    const sidebar = document.getElementById("sidebar");

    if (filter === "NIST CSF Core" && !query) {{
        let html = "<ul>";

        for (const uri of DATA.nistRoots) {{
            html += renderTreeNode(uri, query);
        }}

        html += "</ul>";
        sidebar.innerHTML = html;
        return;
    }}

    const matches = Object.values(concepts)
        .filter(concept => conceptMatches(concept, query, filter))
        .sort((a, b) => displayName(a.uri).localeCompare(displayName(b.uri)));

    const limit = 500;
    let html = "";

    if (!query && filter !== "NIST CSF Core") {{
        html += `<p class="small">Showing first ${{Math.min(limit, matches.length)}} of ${{matches.length}} concepts. Use search to narrow results.</p>`;
    }} else {{
        html += `<p class="small">${{matches.length}} result(s)</p>`;
    }}

    html += "<ul>";

    for (const concept of matches.slice(0, limit)) {{
        html += `<li>${{conceptButton(concept.uri)}}</li>`;
    }}

    html += "</ul>";
    sidebar.innerHTML = html;
}}

function renderList(title, uris) {{
    const cleaned = [...new Set(uris || [])].filter(Boolean);

    if (cleaned.length === 0) return "";

    let html = `
        <div class="card">
            <h3>${{escapeHtml(title)}}</h3>
            <ul>
    `;

    for (const uri of cleaned) {{
        html += `<li>${{conceptButton(uri)}}</li>`;
    }}

    html += `
            </ul>
        </div>
    `;

    return html;
}}

function renderExternalLinks(title, links) {{
    const cleaned = [...new Set(links || [])].filter(Boolean);

    if (cleaned.length === 0) return "";

    let html = `
        <div class="card">
            <h3>${{escapeHtml(title)}}</h3>
            <ul>
    `;

    for (const link of cleaned) {{
        html += `<li><a href="${{escapeHtml(link)}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(link)}}</a></li>`;
    }}

    html += `
            </ul>
        </div>
    `;

    return html;
}}

function renderLiteralList(title, items) {{
    const selectedItems = getLiteralList(items);
    if (!selectedItems || selectedItems.length === 0) return "";

    let html = `
        <div class="card">
            <h3>${{escapeHtml(title)}}</h3>
            <ul>
    `;

    for (const item of selectedItems) {{
        const lang = item.lang ? ` <span class="badge">@${{escapeHtml(item.lang)}}</span>` : "";
        html += `<li>${{escapeHtml(item.value)}}${{lang}}</li>`;
    }}

    html += `
            </ul>
        </div>
    `;

    return html;
}}

function edgeClass(label) {{
    if (["broader", "narrower"].includes(label)) return "hierarchy";
    if (["references", "referenced by"].includes(label)) return "reference";
    if (["exactMatch", "matched by"].includes(label)) return "match";
    if (label === "related") return "related";
    return "";
}}

function addEdge(edges, source, target, label) {{
    if (!source || !target || !concepts[source] || !concepts[target]) return;
    edges.push({{ source, target, label }});
}}

function getEdgesForGraph(uri, type) {{
    const concept = concepts[uri];
    if (!concept) return [];

    let edges = [];

    if (type === "hierarchy") {{
        for (const target of concept.broader || []) addEdge(edges, uri, target, "broader");
        for (const target of concept.narrower || []) addEdge(edges, uri, target, "narrower");
        return edges;
    }}

    if (type === "matches") {{
        for (const target of concept.exactMatch || []) addEdge(edges, uri, target, "exactMatch");
        for (const target of concept.matchedBy || []) addEdge(edges, target, uri, "matched by");
        return edges;
    }}

    if (type === "references") {{
        for (const target of concept.references || []) addEdge(edges, uri, target, "references");
        for (const target of concept.referencedBy || []) addEdge(edges, target, uri, "referenced by");
        for (const target of concept.exactMatch || []) addEdge(edges, uri, target, "exactMatch");
        for (const target of concept.matchedBy || []) addEdge(edges, target, uri, "matched by");

        // Show where referenced NIST concepts sit in the CSF hierarchy.
        if (concept.vocabulary === "NIST CSF Core") {{
            for (const target of concept.broader || []) addEdge(edges, uri, target, "broader");
            for (const target of concept.narrower || []) addEdge(edges, uri, target, "narrower");
        }}

        return edges;
    }}

    // Combined graph.
    for (const target of concept.broader || []) addEdge(edges, uri, target, "broader");
    for (const target of concept.narrower || []) addEdge(edges, uri, target, "narrower");
    for (const target of concept.references || []) addEdge(edges, uri, target, "references");
    for (const target of concept.referencedBy || []) addEdge(edges, target, uri, "referenced by");
    for (const target of concept.exactMatch || []) addEdge(edges, uri, target, "exactMatch");
    for (const target of concept.matchedBy || []) addEdge(edges, target, uri, "matched by");
    for (const target of concept.related || []) addEdge(edges, uri, target, "related");

    return edges;
}}

function buildGraph(rootUri, type, depth) {{
    const nodes = new Map();
    const edgeMap = new Map();
    const queue = [{{ uri: rootUri, depth: 0 }}];
    const visitedAtDepth = new Map();
    const maxNodes = 140;

    while (queue.length > 0 && nodes.size < maxNodes) {{
        const item = queue.shift();

        if (!concepts[item.uri]) continue;

        const previousDepth = visitedAtDepth.get(item.uri);
        if (previousDepth !== undefined && previousDepth <= item.depth) continue;
        visitedAtDepth.set(item.uri, item.depth);

        nodes.set(item.uri, {{ uri: item.uri, depth: item.depth }});

        if (item.depth >= depth) continue;

        const currentEdges = getEdgesForGraph(item.uri, type);

        for (const edge of currentEdges) {{
            const key = `${{edge.source}}|${{edge.label}}|${{edge.target}}`;
            edgeMap.set(key, edge);

            const other = edge.source === item.uri ? edge.target : edge.source;

            if (concepts[other]) {{
                queue.push({{ uri: other, depth: item.depth + 1 }});
            }}
        }}
    }}

    const nodeUris = new Set(nodes.keys());
    const edges = [...edgeMap.values()].filter(edge => nodeUris.has(edge.source) && nodeUris.has(edge.target));

    return {{ nodes: [...nodes.values()], edges }};
}}

function graphNodeClass(uri, rootUri) {{
    const concept = concepts[uri];
    let classes = "graph-node";

    if (uri === rootUri) classes += " root";
    if (concept && concept.vocabulary === "NIST CSF Core") classes += " nist";
    if (concept && concept.vocabulary === "NIST Informative References") classes += " reference";
    if (concept && concept.vocabulary.startsWith("ISO")) classes += " iso";

    return classes;
}}

function graphLabel(uri) {{
    const concept = concepts[uri];
    if (!concept) return uri;

    if (concept.notation) return concept.notation;

    const label = getLiteral(concept.labels) || concept.label || concept.shortUri;
    return label.length > 34 ? label.slice(0, 31) + "..." : label;
}}

function graphDescriptionText(rootUri, graphType, graphDepth, graph) {{
    const root = concepts[rootUri];
    const label = root ? displayName(rootUri) : rootUri;

    return `${{label}} — ${{graph.nodes.length}} node(s), ${{graph.edges.length}} edge(s), depth ${{graphDepth}}, ${{graphType}} graph`;
}}

function computeGraphPositions(graph, width, height) {{
    const centerX = width / 2;
    const centerY = height / 2;
    const byDepth = new Map();

    for (const node of graph.nodes) {{
        if (!byDepth.has(node.depth)) byDepth.set(node.depth, []);
        byDepth.get(node.depth).push(node);
    }}

    const positions = {{}};

    for (const [depth, nodesAtDepth] of byDepth.entries()) {{
        nodesAtDepth.sort((a, b) => displayName(a.uri).localeCompare(displayName(b.uri)));

        if (depth === 0) {{
            positions[nodesAtDepth[0].uri] = {{ x: centerX, y: centerY }};
            continue;
        }}

        const radius = 115 + (depth - 1) * 150;
        const count = nodesAtDepth.length;

        nodesAtDepth.forEach((node, index) => {{
            const angle = (-Math.PI / 2) + (2 * Math.PI * index / Math.max(count, 1));
            positions[node.uri] = {{
                x: centerX + radius * Math.cos(angle),
                y: centerY + radius * Math.sin(angle),
            }};
        }});
    }}

    return positions;
}}

function renderGraphOnly(rootUri) {{
    if (!rootUri || !concepts[rootUri]) {{
        return `
            <div class="card">
                <h2>Select a concept</h2>
                <p>Use the tree or search box on the left, then switch to Graph view.</p>
            </div>
        `;
    }}

    const graphType = document.getElementById("graphType")?.value || "combined";
    const graphDepth = Number(document.getElementById("graphDepth")?.value || 2);
    const graph = buildGraph(rootUri, graphType, graphDepth);

    const width = 1200;
    const height = 760;
    const positions = computeGraphPositions(graph, width, height);

    let html = `
        <div class="card graph-card">
            <div class="graph-title">
                <h2>${{escapeHtml(displayName(rootUri))}}</h2>
                <p>${{escapeHtml(graphDescriptionText(rootUri, graphType, graphDepth, graph))}}</p>
            </div>
            <div class="graph-box">
                <svg id="graphSvg" class="graph-svg" viewBox="0 0 ${{width}} ${{height}}">
                    <g id="graphViewport" transform="translate(${{graphTransform.x}}, ${{graphTransform.y}}) scale(${{graphTransform.scale}})">
    `;

    for (const edge of graph.edges) {{
        const source = positions[edge.source];
        const target = positions[edge.target];
        if (!source || !target) continue;

        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;

        html += `
            <line class="graph-edge ${{edgeClass(edge.label)}}" x1="${{source.x}}" y1="${{source.y}}" x2="${{target.x}}" y2="${{target.y}}"></line>
            <text class="graph-edge-label" x="${{midX}}" y="${{midY}}">${{escapeHtml(edge.label)}}</text>
        `;
    }}

    for (const node of graph.nodes) {{
        const position = positions[node.uri];
        if (!position) continue;

        html += `
            <g class="${{graphNodeClass(node.uri, rootUri)}}" data-graph-uri="${{escapeHtml(node.uri)}}" transform="translate(${{position.x}}, ${{position.y}})">
                <circle r="18"></circle>
                <text text-anchor="middle" y="36">${{escapeHtml(graphLabel(node.uri))}}</text>
            </g>
        `;
    }}

    html += `
                    </g>
                </svg>
                <div class="legend">
                    <div><span class="nist-dot"></span>NIST core</div>
                    <div><span class="ref-dot"></span>Informative reference</div>
                    <div><span class="iso-dot"></span>ISO concept</div>
                </div>
            </div>
        </div>
    `;

    return html;
}}

function applyGraphTransform() {{
    const viewport = document.getElementById("graphViewport");
    if (!viewport) return;
    viewport.setAttribute("transform", `translate(${{graphTransform.x}}, ${{graphTransform.y}}) scale(${{graphTransform.scale}})`);
}}

function zoomGraph(factor) {{
    graphTransform.scale = Math.max(0.25, Math.min(4, graphTransform.scale * factor));
    applyGraphTransform();
}}

function resetGraphZoom() {{
    graphTransform = {{ x: 0, y: 0, scale: 1 }};
    applyGraphTransform();
}}

function setupGraphInteractions() {{
    const svg = document.getElementById("graphSvg");
    if (!svg) return;

    svg.addEventListener("wheel", function(event) {{
        event.preventDefault();
        const factor = event.deltaY < 0 ? 1.12 : 0.88;
        zoomGraph(factor);
    }}, {{ passive: false }});

    svg.addEventListener("pointerdown", function(event) {{
        if (event.target.closest("[data-graph-uri]")) return;
        graphDrag = {{ x: event.clientX, y: event.clientY, startX: graphTransform.x, startY: graphTransform.y }};
        svg.classList.add("dragging");
        svg.setPointerCapture(event.pointerId);
    }});

    svg.addEventListener("pointermove", function(event) {{
        if (!graphDrag) return;
        graphTransform.x = graphDrag.startX + (event.clientX - graphDrag.x);
        graphTransform.y = graphDrag.startY + (event.clientY - graphDrag.y);
        applyGraphTransform();
    }});

    svg.addEventListener("pointerup", function(event) {{
        graphDrag = null;
        svg.classList.remove("dragging");
        try {{ svg.releasePointerCapture(event.pointerId); }} catch (error) {{}}
    }});

    svg.addEventListener("pointerleave", function() {{
        graphDrag = null;
        svg.classList.remove("dragging");
    }});
}}

function renderInfo(rootUri) {{
    if (!rootUri || !concepts[rootUri]) {{
        return `
            <div class="card">
                <h2>Select a concept</h2>
                <p>Use the tree or search box on the left.</p>
            </div>
        `;
    }}

    const concept = concepts[rootUri];
    const definition = getLiteral(concept.definitions) || concept.definition;

    let html = `
        <div class="card">
            <h2>${{escapeHtml(displayName(rootUri))}}</h2>
            <div class="meta">
                <strong>Vocabulary:</strong> ${{escapeHtml(concept.vocabulary)}}<br>
                <strong>Type:</strong> ${{escapeHtml(concept.types.join(", ") || "skos:Concept")}}<br>
                <strong>URI:</strong> <span class="uri">${{escapeHtml(concept.uri)}}</span><br>
                <strong>Short URI:</strong> <span class="uri">${{escapeHtml(concept.shortUri)}}</span><br>
                <strong>Language:</strong> ${{escapeHtml(currentLanguage)}}
            </div>
        </div>
    `;

    if (definition) {{
        html += `
            <div class="card">
                <h3>Definition</h3>
                <p>${{escapeHtml(definition)}}</p>
            </div>
        `;
    }}

    html += renderLiteralList("Implementation Examples", concept.examples);
    html += renderList("Broader Concepts", concept.broader);
    html += renderList("Narrower Concepts", concept.narrower);
    
    const relatedWithoutReferences = (concept.related || []).filter(
        uri => !(concept.references || []).includes(uri));

    html += renderList("Informative References", concept.references);
    html += renderList("Referenced By", concept.referencedBy);

    html += renderList("Exact Matching Concepts", concept.exactMatch);
    html += renderList("Matched By", concept.matchedBy);

    html += renderList("Related Concepts", relatedWithoutReferences);
    html += renderExternalLinks("External Web Pages", concept.seeAlso);

    return html;
}}

function renderDetails() {{
    const uri = getCurrentUri();
    const details = document.getElementById("details");

    if (currentViewMode === "graph") {{
        details.className = "";
        details.innerHTML = renderGraphOnly(uri);
        setupGraphInteractions();
    }} else {{
        details.className = "";
        details.innerHTML = renderInfo(uri);
    }}

    document.getElementById("graphTopControls").classList.toggle("hidden", currentViewMode !== "graph");
    renderSidebar();
}}

populateLanguageSelect();
renderSidebar();
renderDetails();
</script>
</body>
</html>
"""

    html = html.replace("{{", "{").replace("}}", "}")
    html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False, indent=2))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    print(f"Created {OUTPUT_FILE}")
    print(f"Concepts loaded: {len(concepts)}")
    print(f"NIST top concepts: {len(nist_roots)}")
    print(f"Languages loaded: {', '.join(data['languages'])}")


if __name__ == "__main__":
    main()