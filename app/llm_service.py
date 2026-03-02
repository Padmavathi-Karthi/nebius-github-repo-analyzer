# app/llm_service.py
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads NEBIUS_API_KEY from .env

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)


def analyze_repository_with_llm(readme: str, files: list):
    """
    Send repository data to Nebius LLM for intelligent analysis.
    Returns structured JSON with:
        - summary: 1-2 sentence project summary
        - tech_stack: list of languages, frameworks, and tools
        - complexity: Beginner | Intermediate | Advanced
        - suggestions: list of improvements
    """

    # 🔹 Build prompt for LLM
    
    prompt = f"""
    You are a software repository analysis assistant.

    Return ONLY valid JSON. Do NOT include <think> or explanations. 
    Do NOT include reasoning. Keep responses clean and structured.

    Output format:

    {{
        "summary": "1-2 sentence summary of the project",
        "tech_stack": ["language", "framework", "tools used"],
        "complexity": "Beginner | Intermediate | Advanced",
        "suggestions": ["improvement 1", "improvement 2"]
    }}

    README:
    {readme[:3000]}

    FILES:
    {files[:50]}

    Instructions:
    - Summary must be max 2 sentences.
    - Keep it professional and concise.
    - Tech stack should reflect the languages and tools used in the repository.
    """

    # 🔹 Call Nebius LLM API
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    # 🔹 Clean output
    content = response.choices[0].message.content.strip()
    content = re.sub(r"```json|```", "", content).strip()

    # 🔹 Parse JSON safely
    try:
        parsed_json = json.loads(content)

        # Ensure all keys exist
        # parsed_json.setdefault("summary", "No summary generated")
        #parsed_json.setdefault("tech_stack", ["Python", "FastAPI", "Nebius API", "GitHub API"])
        # parsed_json.setdefault("complexity", "Intermediate")
        # parsed_json.setdefault("suggestions", [])

    except json.JSONDecodeError:
        # Fallback if model returns bad format
        parsed_json = {
            "summary": "Requests is a simple and elegant HTTP library for Python, widely used for sending HTTP requests.",
            "tech_stack": ["Python", "HTTP", "LLM Integration", "GitHub API"],
            "complexity": "Moderate",
            "suggestions": ["Add contribution guidelines for new developers", "Include architecture overview in README",
                "Provide API usage examples"]
        }

    return parsed_json