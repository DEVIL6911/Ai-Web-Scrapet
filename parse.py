import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = "gemini-2.5-flash"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"

def call_gemini(prompt_text, max_output_tokens=3000):
    """Send prompt to Gemini API and return response text."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in environment or Streamlit secrets.")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    payload = {
        "contents": [
            {"parts": [{"text": prompt_text}]}
        ],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens
        }
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except KeyError:
        return ""

def parse_with_gemini(dom_chunks, parse_description):
    """Extract specific info from webpage chunks using Gemini."""
    results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = (
            f"You are tasked with extracting specific information from the following text content:\n\n{chunk}\n\n"
            f"Please follow these instructions carefully:\n"
            f"1. Extract only the information that matches this description: {parse_description}\n"
            f"2. Do NOT include extra explanations or formatting.\n"
            f"3. If no match is found, return an empty string ('')."
        )
        print(f"🔹 Processing batch {i}/{len(dom_chunks)}...")
        result = call_gemini(prompt)
        results.append(result)
    return "\n".join(results)

