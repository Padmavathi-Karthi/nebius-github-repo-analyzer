# app/github_service.py
import requests

ASSESSMENT_FILES = [
        "main.py",
        "llm_service.py",
        "github_service.py",
        "requirements.txt",
        "README.md"
    ]

GITHUB_API_BASE = "https://api.github.com/repos"

def get_repo_files(owner: str, repo: str, path=""):
    """
    Fetch GitHub repo files, return only files relevant for this assessment.
    """


    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    res = requests.get(url)
    all_files = []
    important_files = []

    if res.status_code == 200:
        data = res.json()
        for item in data:
            if item["type"] == "dir":
                # Recursively fetch directory contents
                sub_files = get_repo_files(owner, repo, item["path"])
                all_files.extend(sub_files["files"])
                important_files.extend(sub_files["important_files"])
            else:
                fname = item["name"]
                all_files.append(fname)
                if fname in ASSESSMENT_FILES:
                    important_files.append(fname)

    return {
        "files": all_files,
        "important_files": important_files
    }