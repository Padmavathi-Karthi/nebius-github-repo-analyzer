# app/main.py
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests

from app.github_service import get_repo_files
from app.llm_service import analyze_repository_with_llm

load_dotenv()

app = FastAPI(
    title="AI GitHub Repository Analyzer",
    version="1.0.0",
)


# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI GitHub Repository Analyzer is running"
    }


# ---------------------------------------------------------------------
# Repository Analysis Endpoint
# ---------------------------------------------------------------------

@app.get("/analyze")
def analyze_repo(owner: str, repo: str):
    """
    Analyze a public GitHub repository using Nebius LLM.
    """

    try:
        # -------------------------------------------------------------
        # Step 1: Fetch repository file structure
        # -------------------------------------------------------------

        repo_data = get_repo_files(owner, repo)

        all_files = repo_data.get("files", [])
        important_files = repo_data.get("important_files", [])

        if not all_files:
            raise HTTPException(
                status_code=404,
                detail="Repository not found or contains no accessible files.",
            )

        # -------------------------------------------------------------
        # Step 2: Fetch README content
        # -------------------------------------------------------------

        readme_file = next(
            (f for f in all_files if "readme" in f.lower()),
            None,
        )

        readme_content = ""

        if readme_file:
            readme_url = (
                f"https://raw.githubusercontent.com/"
                f"{owner}/{repo}/main/{readme_file}"
            )

            response = requests.get(readme_url, timeout=10)

            if response.status_code == 200:
                readme_content = response.text

        # -------------------------------------------------------------
        # Step 3: Generate LLM analysis
        # -------------------------------------------------------------

        ai_analysis = analyze_repository_with_llm(
            readme=readme_content,
            files=all_files,
        )

        # -------------------------------------------------------------
        # Step 4: Return structured response
        # -------------------------------------------------------------

        return {
            "repository": f"{owner}/{repo}",
            "important_files": important_files,
            "ai_analysis": ai_analysis,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Repository analysis failed: {str(e)}",
        )
