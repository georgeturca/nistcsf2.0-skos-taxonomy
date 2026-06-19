# Code by georgeturca
#NIST CSF 2.0 taxonomy build pipeline.
#Extracts the NIST CSF Core data, builds the
#RDF/SKOS taxonomy, generates the local browser, and starts a local web
#server so the browser.



from pathlib import Path
import subprocess
import sys
import webbrowser


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = PROJECT_ROOT / "src" / "pipeline"

BROWSER_PORT = 8000
BROWSER_URL = f"http://localhost:{BROWSER_PORT}"


def run_step(script_name: str, description: str) -> None:
    """Run one script from the pipeline directory."""
    script_path = PIPELINE_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Could not find pipeline step: {script_path}")

    print()
    print("=" * 80)
    print(description)
    print("=" * 80)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )


def start_browser_server() -> None:
    """Start a local HTTP server for the generated browser."""
    print()
    print("=" * 80)
    print("Build finished. Starting local taxonomy browser.")
    print("=" * 80)
    print(f"You can view the taxonomy browser at: {BROWSER_URL}")
    print("Press Ctrl+C to stop the browser server.")

    webbrowser.open(BROWSER_URL)

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "http.server",
                str(BROWSER_PORT),
                "-d",
                "website",
            ],
            cwd=PROJECT_ROOT,
            check=True,
        )
    except KeyboardInterrupt:
        print("\nBrowser server stopped.")


def main() -> None:
    """Create output folders, run the build steps, and open the browser."""
    print("Building NIST CSF 2.0 SKOS taxonomy project...")

    (PROJECT_ROOT / "output").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "website").mkdir(parents=True, exist_ok=True)

    run_step(
        "extract_csf_core.py",
        "Step 1: Extract multilingual NIST CSF Core CSV",
    )

    run_step(
        "build_taxonomy.py",
        "Step 2: Build RDF/SKOS Turtle taxonomy",
    )

    run_step(
        "build_browser.py",
        "Step 3: Build local HTML taxonomy browser",
    )

    start_browser_server()


if __name__ == "__main__":
    main()