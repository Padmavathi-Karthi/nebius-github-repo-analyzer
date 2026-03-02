# GitHub Repository Analyser API (Nebius LLM)

## Overview

This project is an AI-powered backend service that analyses any public GitHub repository using a Large Language Model (LLM) via the Nebius API.  
It fetches repository metadata, identifies important files, and generates a structured, human-readable analysis including summary, tech stack, complexity, and improvement suggestions.

This project was developed as part of the **Nebius Academy Assessment**, demonstrating integration of LLM APIs, backend engineering, and structured AI outputs.

---

## Key Features

- Analyse any public GitHub repository
- Uses Nebius LLM for intelligent codebase analysis
- Extracts important project files automatically
- Returns structured and human-readable JSON output
- Clean FastAPI backend architecture
- Environment variable based secure API key handling

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

nebius_github_repo_api/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── llm_service.py # Nebius LLM integration
│ ├── github_service.py # GitHub API logic
│
├── .env.example #.env is not committed
├── requirements.txt # Project dependencies
└── README.md # Project documentation

---

## How It Works

1. User sends a request with GitHub repo details
2. Backend fetches:
   - README
   - File structure
   - Important configuration files
3. Data is sent to Nebius LLM
4. LLM generates structured analysis
5. API returns a clean JSON response

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
    "complexity": "Moderate",
    "suggestions": [
      "Add contribution guidelines for new developers",
      "Include architecture overview in README",
      "Provide API usage examples"
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

## Design Decisions

- Separated GitHub and LLM logic into independent service modules
- Implemented safe JSON parsing to prevent API crashes
- Limited LLM input to essential repository data for performance
- Structured output schema for predictable API responses

---
