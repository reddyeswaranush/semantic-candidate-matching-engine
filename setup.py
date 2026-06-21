# setup.py
import os
import json
from pathlib import Path

def create_dirs():
    dirs = [
        "storage",
        "data/embeddings",
        "data/indexes",
        "data/processed",
        "outputs"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✓ {d}/")

def create_storage():
    storage_file = Path("storage/uploaded_candidates.json")
    if not storage_file.exists():
        with open(storage_file, "w") as f:
            json.dump([], f)
        print("✓ storage/uploaded_candidates.json")
    else:
        print("~ storage/uploaded_candidates.json already exists")

def create_gitkeeps():
    gitkeep_dirs = [
        "storage",
        "data/embeddings",
        "data/indexes",
        "outputs"
    ]
    for d in gitkeep_dirs:
        gk = Path(d) / ".gitkeep"
        gk.touch()
        print(f"✓ {d}/.gitkeep")

def create_gitignore():
    gitignore_path = Path(".gitignore")
    entries = [
        "storage/uploaded_candidates.json",
        "data/embeddings/",
        "data/indexes/",
        "outputs/",
        "__pycache__/",
        "*.pyc",
        ".env"
    ]
    existing = []
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            existing = f.read().splitlines()

    with open(gitignore_path, "a") as f:
        for entry in entries:
            if entry not in existing:
                f.write(f"\n{entry}")
                print(f"✓ .gitignore ← {entry}")

def build_index():
    print("\nBuilding embeddings + index...")
    from src.storage_manager import total_candidates
    if total_candidates() == 0:
        print("⚠ No candidates in storage. Upload candidates first, then re-run setup.")
        return
    from src.full_embeddings import generate_full_embeddings
    from src.full_retrieval import build_full_index
    generate_full_embeddings()
    build_full_index()
    print("✓ Index built")

if __name__ == "__main__":
    print("=== Setup ===\n")
    print("Creating directories...")
    create_dirs()
    print("\nInitializing storage...")
    create_storage()
    print("\nCreating .gitkeeps...")
    create_gitkeeps()
    print("\nUpdating .gitignore...")
    create_gitignore()
    build_index()
    print("\n=== Done. Run: streamlit run app.py ===")