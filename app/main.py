# app/main.py
import requests
from fastapi import FastAPI
from app.github_service import get_repo_files
from app.llm_service import analyze_repository_with_llm
from dotenv import load_dotenv

load_dotenv()  # Load NEBIUS_API_KEY

app = FastAPI(title="AI GitHub Repo Analyzer (Nebius)")


@app.get("/")
def home():
    return {"message": "Nebius AI Repo Analyzer is running 🚀"}


@app.get("/analyze")
def analyze_repo(owner: str, repo: str):
    """
    Full AI-powered repo analysis
    Example:
    /analyze?owner=psf&repo=requests
    """
    # Step 1: Fetch GitHub repo data
    repo_data = get_repo_files(owner, repo)
    all_files = repo_data.get("files", [])
    important_files = repo_data.get("important_files", [])

    # Step 2: Fetch README content
    readme_file_name = next(
        (f for f in all_files if "readme" in f.lower()), None
    )

    readme_content = ""
    if readme_file_name:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{readme_file_name}"
        res = requests.get(url)
        if res.status_code == 200:
            readme_content = res.text

    # Step 3: Send data to Nebius LLM for analysis
    ai_analysis = analyze_repository_with_llm(
        readme=readme_content,
        files=all_files
    )

    # Step 4: Return clean, structured JSON
    return {
        "repository": f"{owner}/{repo}",
        "important_files": ["README.md", "requirements.txt", "main.py", "llm_service.py", "github_service.py"],
        "ai_analysis": ai_analysis
    }
print("DEBUG: THIS MAIN FILE IS RUNNING")