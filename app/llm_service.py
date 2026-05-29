# app/llm_service.py
import os
import json
import re
from typing import List, Dict, Any

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads NEBIUS_API_KEY from .env

# ---------------------------------------------------------------------
# LLM Client (Nebius OpenAI-compatible endpoint)
# ---------------------------------------------------------------------

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
)

# ---------------------------------------------------------------------
# Prompt Builder
# ---------------------------------------------------------------------

def build_prompt(readme: str, files: List[str]) -> str:
    return f"""
You are a precise software repository analysis engine.

Your task:
Analyze the repository input and return ONLY valid JSON.

STRICT OUTPUT RULES:
- Output must be valid JSON only
- No explanations
- No markdown
- No reasoning steps
- No extra text

JSON FORMAT:
{{
  "summary": "1-2 sentence description of the project",
  "tech_stack": ["languages", "frameworks", "tools"],
  "complexity": "Beginner | Intermediate | Advanced",
  "suggestions": ["improvement 1", "improvement 2"]
}}

REPOSITORY README:
{readme[:3000]}

REPOSITORY FILES:
{files[:50]}
""".strip()


# ---------------------------------------------------------------------
# Safe JSON Parsing
# ---------------------------------------------------------------------

def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON safely from model output.
    Handles accidental backticks or extra text.
    """
    if not text:
        raise ValueError("Empty LLM response")

    # Remove markdown code blocks if present
    cleaned = text.strip()
    cleaned = re.sub(r"```json|```", "", cleaned).strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # fallback: extract first JSON object
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


# ---------------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------------

def analyze_repository_with_llm(readme: str, files: list) -> Dict[str, Any]:
    """
    Sends repository data to Nebius LLM and returns structured analysis.
    """

    prompt = build_prompt(readme, files)

    last_error = None

    for attempt in range(2):  # simple retry for robustness
        try:
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-0528",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict JSON generator for repository analysis. "
                            "Always return valid JSON only."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=600,
            )

            content = response.choices[0].message.content.strip()
            return extract_json(content)

        except Exception as e:
            last_error = e
            continue

    # -----------------------------------------------------------------
    # Graceful fallback (non-fake, safe default)
    # -----------------------------------------------------------------

    return {
        "summary": "Failed to generate structured analysis from LLM response.",
        "tech_stack": [],
        "complexity": "Unknown",
        "suggestions": [
            "Check LLM response format",
            "Improve prompt consistency",
            "Retry analysis request",
        ],
        "error": str(last_error),
    }
