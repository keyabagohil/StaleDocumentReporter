import ast, pathlib, javalang

def extract_symbols_from_files(paths):
    out = set()
    for p in paths:
        pp = pathlib.Path(p)
        try:
            txt = pp.read_text(errors="ignore")
        except Exception:
            continue
        if pp.suffix == ".py":
            try:
                tree = ast.parse(txt)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if not node.name.startswith("_"):
                            out.add(node.name)
            except Exception:
                pass
        elif pp.suffix == ".java":
            try:
                tree = javalang.parse.parse(txt)
                for _, cls in tree.filter((javalang.tree.ClassDeclaration,
                                           javalang.tree.InterfaceDeclaration,
                                           javalang.tree.EnumDeclaration)):
                    if 'public' in getattr(cls, 'modifiers', set()):
                        out.add(cls.name)
                for _, m in tree.filter(javalang.tree.MethodDeclaration):
                    if 'public' in getattr(m, 'modifiers', set()):
                        out.add(m.name)
            except Exception:
                pass
    return out
