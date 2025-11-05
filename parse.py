# file: parse_with_gemini.py

import os
import requests
import json

# --- Configuration ---
GEMINI_API_KEY = os.getenv("AIzaSyDS87MdLl5vWL6JuSvWZ7BMgU59L7qVzKQ")  # Set this in your environment / secrets
MODEL_ID = "gemini-2.5-flash"  # Using the Flash model as per docs. :contentReference[oaicite:3]{index=3}
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent".format(model=MODEL_ID)

# --- Helpers ---
def call_gemini(prompt_text: str, thinking_budget: int = None, max_output_tokens: int = 512) -> str:
    """
    Call the Gemini API and return the generated text.
    :param prompt_text: The text prompt to send.
    :param thinking_budget: Optional internal “thinking” budget (depending on model).
    :param max_output_tokens: Maximum tokens to output.
    :return: Generated text.
    """
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens
        }
    }
    # If thinking_budget is supported by the model, include it
    if thinking_budget is not None:
        body["generationConfig"]["thinkingBudget"] = thinking_budget

    response = requests.post(API_ENDPOINT, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    # Depending on API version, the generated text might be under different fields:
    # Example: data["candidates"][0]["output"] or data["candidates"][0]["text"]
    try:
        return data["candidates"][0]["output"]
    except KeyError:
        return data["candidates"][0].get("text", "")

# --- Integration with your parsing chain ---
def parse_with_gemini(dom_chunks, parse_description: str) -> str:
    """
    Splits DOM chunks, calls Gemini for each chunk, and returns combined results.
    :param dom_chunks: List of strings (chunks of DOM content).
    :param parse_description: What to extract.
    :return: Concatenated results.
    """
    results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = (
            "You are tasked with extracting specific information from the following text content: {dom_content}. "
            "Please follow these instructions carefully: \n\n"
            "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
            "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
            "3. **Empty Response:** If no information matches the description, return an empty string ('')."
        ).format(dom_content=chunk, parse_description=parse_description)

        # You can optionally set a thinking budget for the model, e.g., 100 tokens
        result = call_gemini(prompt, thinking_budget=100, max_output_tokens=3000)
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        results.append(result.strip())

    return "\n".join(results)

# --- Example Usage ---
if __name__ == "__main__":
    # Example chunk list (in your real code replace this with actual split DOM content)
    example_chunks = [
        "Some HTML-extracted body content chunk #1 ...",
        "Some HTML-extracted body content chunk #2 ..."
    ]
    description = "List all email addresses found in the content."
    output = parse_with_gemini(example_chunks, description)
    print("Parsed result:\n", output)
