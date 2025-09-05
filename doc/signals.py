import os
from git import Repo

def _last_commit_ts_for_paths(repo: Repo, paths):
    """
    Return the latest commit timestamp among the given file paths.
    IMPORTANT: convert absolute paths to repo-relative paths so GitPython can find history.
    """
    if not paths:
        return 0
    root = repo.working_tree_dir
    latest = 0
    for p in paths:
        try:
            rel = os.path.relpath(p, root) if os.path.isabs(p) else p
            # Normalize path separators for Git on Windows/macOS/Linux
            rel = rel.replace(os.sep, "/")
            commits = list(repo.iter_commits(paths=rel, max_count=1))
            if commits:
                latest = max(latest, commits[0].committed_date)
        except Exception:
            # ignore files Git can't resolve (deleted/renamed/etc.)
            pass
    print("Latest commit ts for paths:", latest)
    return latest

def last_change_times(repo_dir, code_paths, doc_paths):
    """
    Returns (code_ts, docs_ts) as Unix timestamps.
    code_ts: latest commit touching any *code* file.
    docs_ts: latest commit touching any *doc* file.
    """
    repo = Repo(repo_dir)
    code_ts = _last_commit_ts_for_paths(repo, code_paths)
    docs_ts = _last_commit_ts_for_paths(repo, doc_paths)
    return code_ts, docs_ts

