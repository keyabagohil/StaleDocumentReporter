from git import Repo
import os

def shallow_clone_or_pull(repo_url, branch, dest):
    if not os.path.isdir(dest) or not os.path.isdir(os.path.join(dest, ".git")):
        repo = Repo.clone_from(repo_url, dest, branch=branch, depth=1)
    else:
        repo = Repo(dest)
        repo.remote().set_url(repo_url)
        repo.git.fetch(depth=1)
        repo.git.checkout(branch)
        repo.git.reset("--hard", f"origin/{branch}")
    return repo.head.commit.hexsha[:7]
