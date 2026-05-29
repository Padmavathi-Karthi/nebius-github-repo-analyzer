# GitHub Repository Analyser API (Nebius LLM)

## Overview

An AI-powered backend service that analyzes public GitHub repositories using Nebius-hosted Large Language Models (LLMs).

The system fetches repository metadata, extracts important project files, and generates structured repository insights including summaries, technology stack analysis, complexity assessment, and improvement suggestions.

---

## Key Features

- Analyze any public GitHub repository
- AI-generated repository summaries using Nebius LLMs
- Automatic extraction of important project files
- Structured JSON responses for downstream integrations
- FastAPI-based backend architecture
- Secure environment-variable API key management

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **LLM Provider:** Nebius API
- **HTTP Client:** Requests
- **Server:** Uvicorn
- **Environment Management:** python-dotenv
- **Version Control:** Git & GitHub 

---

## Project Structure

```text
nebius_github_repo_api/
│
├── app/
│ ├── main.py                # FastAPI entry point
│ ├── llm_service.py         # Nebius LLM integration
│ ├── github_service.py      # GitHub API logic
│
├── .env.example             #.env is not committed
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```
---

## API Endpoint

### Analyze a Repository

**GET**
/analyze?owner=<repo_owner>&repo=<repo_name>

### Example Request

http://127.0.0.1:8000/analyze?owner=psf&repo=requests

### Example Response

```json
{
  "repository": "psf/requests",
  "important_files": [
    "README.md",
    "requirements.txt",
    "main.py",
    "llm_service.py",
    "github_service.py"
  ],
  "ai_analysis": {
    "summary": "Requests is a simple and elegant HTTP library for Python, widely used for sending HTTP requests.",
    "tech_stack": ["Python", "FastAPI", "Nebius API", "GitHub API"],
    "complexity": "Intermediate",
    "suggestions": [
      "Add contribution guidelines",
      "Improve architecture documentation"
    ]
  }
}
```

---

## Installation

```bash
git clone <repository_url>
cd nebius_github_repo_api
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Create a '.env' file:

```env
NEBIUS_API_KEY=\*\*\*\*
```

## Run the server:

```bash
uvicorn app.main:app --reload
```
---

## System Workflow

1. Client submits repository details
2. Backend fetches repository metadata and important files
3. Repository context is sent to the Nebius LLM
4. The LLM generates structured repository analysis
5. API returns JSON-based insights

---

## Design Decisions

- Modular separation between GitHub services and LLM orchestration
- Structured response schema for predictable outputs
- Controlled repository context extraction for reduced token usage
- Safe JSON parsing and error handling for API reliability

---

## Future Improvements

- Support for private repositories via OAuth
- Repository embedding and semantic search
- Streaming LLM responses
- Async GitHub API fetching
- Persistent analysis caching
