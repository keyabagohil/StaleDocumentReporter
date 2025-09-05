import os, json, re, pathlib
from datetime import datetime, timezone
from git_client import shallow_clone_or_pull
from discover import list_docs_and_code
from symbols import extract_symbols_from_files
from docs import read_all_docs_concat, count_broken_links, claimed_versions_in_docs
from signals import last_change_times
from score import compute_score
from .llm import generate_suggestions_or_empty

ROOT = "/tmp/docfresh"
REPO_DIR = os.path.join(ROOT, "repo")
SCANS_DIR = os.path.join(ROOT, "scans")
REPORT_LATEST = os.path.join(ROOT, "report.json")

def infer_repo_name(url):
    m = re.search(r'github\.com/([^/]+/[^/.]+)', url)
    return m.group(1) if m else url

def detect_repo_versions(repo_dir):
    out = {}
    p = pathlib.Path(repo_dir)
    for f in ["pyproject.toml", "runtime.txt", ".python-version", "Dockerfile"]:
        fp = p/f
        if fp.exists():
            t = fp.read_text(errors="ignore")
            m = re.search(r'python[^0-9]*([\d]+\.[\d]+)', t, re.I)
            if m: out["python"] = m.group(1)
    pom = p/"pom.xml"
    if pom.exists():
        t = pom.read_text(errors="ignore")
        m = re.search(r'<maven\.compiler\.source>([\d\.]+)</maven\.compiler\.source>', t)
        if m: out["java"] = m.group(1)
    return out

def run_scan(repo_url, branch="main", reason="manual"):
    os.makedirs(ROOT, exist_ok=True)
    os.makedirs(SCANS_DIR, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()

    commit = shallow_clone_or_pull(repo_url, branch, REPO_DIR)
    docs, code = list_docs_and_code(REPO_DIR)
    code_ts, docs_ts = last_change_times(REPO_DIR, code, docs)
    print("ethar")
    print(code_ts, docs_ts)
    delta_days = (code_ts - docs_ts) / 86400.0
    age_gap_days = max(0.0, delta_days)
    docs_lead_days = max(0.0, -delta_days)
    # no_docs = (len(docs) == 0)
    # if code_ts and docs_ts:
    #     delta_days = (code_ts - docs_ts) / 86400.0
    #     age_gap_days = round(max(0.0, delta_days), 2)
    #     docs_lead_days = round(max(0.0, -delta_days), 2)
    # elif code_ts and not docs_ts:
    #     # code exists, docs exist but Git couldn’t find commits? treat as fully behind
    #     age_gap_days = round((code_ts - 0) / 86400.0, 2)
    #     docs_lead_days = 0.0
    # elif docs_ts and not code_ts:
    #     # docs newer than any code commit we detected (edge repo), treat as docs leading
    #     age_gap_days = 0.0
    #     docs_lead_days = round((docs_ts - 0) / 86400.0, 2)
    # else:
    #     age_gap_days = 0.0
    #     docs_lead_days = 0.0

    print("*"*10,docs_lead_days)
    age_gap_days = max(0.0, (code_ts - docs_ts)/86400.0)
    print("Age gap days:", age_gap_days)
    symbols = extract_symbols_from_files(code)
    doc_text = read_all_docs_concat(docs)
    mentioned = sum(1 for s in symbols if re.search(rf'(`{re.escape(s)}`|\b{re.escape(s)}\b)', doc_text))
    coverage = 100.0 * (mentioned / max(1, len(symbols)))

    broken_links = count_broken_links(doc_text, max_links=20, timeout=2)

    claimed = claimed_versions_in_docs(doc_text)
    detected = detect_repo_versions(REPO_DIR)
    version_skew = {k: {"docs": v, "repo": detected.get(k)} for k,v in claimed.items()}

    score = compute_score(age_gap_days, coverage, broken_links, version_skew)
    finished = datetime.now(timezone.utc).isoformat()
    repo_name = infer_repo_name(repo_url)

    report = {
      "repo": repo_name,
      "branch": branch,
      "commit": commit,
      "started_at": started,
      "finished_at": finished,
      "trigger": reason,                         # <-- NEW: manual/cron/webhook
      "repo_score": round(score, 3),
      "metrics": {
        "age_gap_days": round(age_gap_days, 2),
        "api_coverage_pct": round(coverage, 1),
        "broken_links": int(broken_links),
        "version_skew": version_skew
      }
    }
    report["llm_suggestions"] = generate_suggestions_or_empty(report)

    with open(REPORT_LATEST, "w") as f: json.dump(report, f, indent=2)
    fname = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{reason}.json"  # include reason in filename
    with open(os.path.join(SCANS_DIR, fname), "w") as f: json.dump(report, f, indent=2)
    return report

    # with open(REPORT_LATEST, "w") as f: json.dump(report, f, indent=2)
    # fname = datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
    # with open(os.path.join(SCANS_DIR, fname), "w") as f: json.dump(report, f, indent=2)
    # return report
