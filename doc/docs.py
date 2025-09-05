import re, pathlib, requests

def read_all_docs_concat(doc_paths):
    parts = []
    for p in doc_paths:
        try:
            parts.append(pathlib.Path(p).read_text(errors="ignore"))
        except Exception:
            pass
    return "\n\n".join(parts)

def count_broken_links(text, max_links=20, timeout=2):
    urls = re.findall(r'\bhttps?://[^\s)\]]+', text)
    urls = list(dict.fromkeys(urls))[:max_links]
    bad = 0
    for u in urls:
        try:
            r = requests.head(u, timeout=timeout, allow_redirects=True)
            if r.status_code >= 400:
                r = requests.get(u, timeout=timeout, allow_redirects=True)
            bad += 1 if r.status_code >= 400 else 0
        except Exception:
            bad += 1
    return bad

def claimed_versions_in_docs(text):
    out = {}
    m = re.search(r'Python\s*(\d+\.\d+)', text, re.I);   out["python"] = m.group(1) if m else None
    m = re.search(r'Java\s*(\d+\.\d+|\d+)', text, re.I); out["java"]   = m.group(1) if m else None
    return {k:v for k,v in out.items() if v}

