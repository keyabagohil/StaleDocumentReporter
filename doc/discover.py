import pathlib
DOC_EXT = {".md", ".rst"}
CODE_EXT = {".py", ".java"}

def is_doc(p: pathlib.Path):
    parts = [s.lower() for s in p.parts]
    return p.suffix in DOC_EXT or "docs" in parts or p.name.lower().startswith("readme")

def is_code(p: pathlib.Path):
    return p.suffix in CODE_EXT

def list_docs_and_code(root):
    rootp = pathlib.Path(root)
    files = [p for p in rootp.rglob("*") if p.is_file() and ".git" not in p.parts]
    docs = [str(p) for p in files if is_doc(p)]
    code = [str(p) for p in files if is_code(p)]
    return docs, code
