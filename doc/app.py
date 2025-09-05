import os, json, threading, hmac, hashlib
from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from scanner.run import run_scan, REPORT_LATEST, SCANS_DIR

app = Flask(__name__)
app.config["REPO_URL"] = os.getenv("REPO_URL", "").strip()
app.config["BRANCH"] = os.getenv("BRANCH", "main").strip()
app.config["WEBHOOK_SECRET"] = os.getenv("GITHUB_WEBHOOK_SECRET", "").strip()

_scan_lock = threading.Lock()

def safe_scan(reason="manual"):
    if not app.config["REPO_URL"]:
        return None
    if _scan_lock.locked():  # skip overlapping scans
        return None
    with _scan_lock:
        return run_scan(app.config["REPO_URL"], app.config["BRANCH"])

# -------- UI --------
# @app.get("/")
# def index():
#     latest = None
#     if os.path.exists(REPORT_LATEST):
#         latest = json.load(open(REPORT_LATEST))
#     return render_template("index.html",
#                            repo_url=app.config["REPO_URL"],
#                            branch=app.config["BRANCH"],
#                            latest=latest)

@app.get("/")
def index():
    latest = None
    if os.path.exists(REPORT_LATEST):
        latest = json.load(open(REPORT_LATEST))
    # build a small history list from SCANS_DIR (last 15 files)
    history = []
    if os.path.isdir(SCANS_DIR):
        for name in sorted(os.listdir(SCANS_DIR), reverse=True)[:15]:
            try:
                history.append(json.load(open(os.path.join(SCANS_DIR, name))))
            except Exception:
                pass
    return render_template("index.html",
                           repo_url=app.config["REPO_URL"],
                           branch=app.config["BRANCH"],
                           latest=latest,
                           history=history)

@app.get("/history")
def history():
    items = []
    if os.path.isdir(SCANS_DIR):
        for name in sorted(os.listdir(SCANS_DIR), reverse=True)[:50]:
            try:
                items.append(json.load(open(os.path.join(SCANS_DIR, name))))
            except Exception:
                pass
    return jsonify(items)


# Manual scan
@app.post("/scan")
def scan():
    data = request.get_json(force=True)
    # allow changing repo from UI once
    if "repo_url" in data:
        app.config["REPO_URL"] = data["repo_url"].strip()
    if "branch" in data:
        app.config["BRANCH"] = data["branch"].strip() or "main"
    res = safe_scan("manual")
    return jsonify({"ok": bool(res)}), (200 if res else 202)

# Latest report JSON
@app.get("/report")
def report():
    if not os.path.exists(REPORT_LATEST):
        return jsonify({"error":"no report yet"}), 404
    return json.load(open(REPORT_LATEST))

# -------- Cron every 5 minutes --------
sched = BackgroundScheduler(daemon=True)
@sched.scheduled_job("interval", minutes=2)
def cron_scan():
    print("[CRON] Triggered at", __import__("datetime").datetime.now())
    res = safe_scan("cron")
    if res:
        # return render_template("index.html",
        #                    repo_url=app.config["REPO_URL"],
        #                    branch=app.config["BRANCH"],
        #                    cron=res)
        print("[CRON] Scan finished:", res["commit"], "score", res["repo_score"])
    else:
        print("[CRON] Scan skipped (maybe running already)")
sched.start()

# -------- GitHub webhook (push -> scan) --------
def _verify_signature(body, header_sig, secret):
    if not secret:  # no secret configured -> accept (hackathon mode)
        return True
    if not header_sig or not header_sig.startswith("sha256="):
        return False
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest("sha256="+digest, header_sig)

@app.post("/webhook/github")
def github_webhook():
    event = request.headers.get("X-GitHub-Event","")
    signature = request.headers.get("X-Hub-Signature-256","")
    if not _verify_signature(request.data, signature, app.config["WEBHOOK_SECRET"]):
        return "bad signature", 401
    if event == "push":
        safe_scan("webhook")
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
