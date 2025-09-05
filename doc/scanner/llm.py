# scanner/llm.py
import os, json
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_suggestions_or_empty(report: dict) -> List[str]:
    """
    Returns a small list of suggestion bullets using Google Gemini.
    - Only runs if GEMINI_API_KEY is present; otherwise returns [].
    - Cheap + fast: short prompt, low max tokens.
    Env:
      GEMINI_API_KEY  (required to enable)
      GEMINI_MODEL    (optional, default: gemini-1.5-flash)
      GEMINI_BASE_URL (optional, default: https://generativelanguage.googleapis.com)
    """
    os.environ["GOOGLE_API_KEY"] = "AIzaSyAFFMG901var8JIMIygaDP9SN9cZZltZlA"

    llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    )

    # if not api_key:
    #     return []

    # try:
    #     import requests

    #     # base = "https://generativelanguage.googleapis.com"
    #     # model = "gemini-2.5-flash"
    #     # url = f"{base}/v1beta/models/{model}:generateContent?key={api_key}"

    prompt = (
        "You are a senior technical writer. Given this repository scan summary JSON, "
        "suggest 2-3 concise, actionable documentation edits to improve freshness. "
        "Keep each suggestion short; no numbering.\n\n"
        f"REPORT JSON:\n{json.dumps(report, indent=2)}\n\n"
        "Respond as plain text bullets, one per line (start with '-' or '•')."
    )

    response = llm_gemini.invoke(prompt)
    print(response.content)
    return [response.content]
    #     payload = {
    #         "contents": [
    #             {"role": "user", "parts": [{"text": prompt}]}
    #         ],
    #         "generationConfig": {
    #             "temperature": 0.2,
    #             "maxOutputTokens": 200
    #         }
    #     }

    #     r = requests.post(url, json=payload, timeout=12)
    #     r.raise_for_status()
    #     data = r.json()

    #     # Gemini response shape: candidates[0].content.parts[*].text
    #     text = ""
    #     candidates = data.get("candidates") or []
    #     if candidates:
    #         parts = (candidates[0].get("content") or {}).get("parts") or []
    #         text = "".join(p.get("text", "") for p in parts).strip()

    #     if not text:
    #         return []

    #     # Split into clean bullets
    #     lines = [ln.strip(" -*•\t") for ln in text.splitlines() if ln.strip()]
    #     return [ln for ln in lines if ln]
    # except Exception:
    #     # Fail closed: no suggestions if any error
    #     return []

