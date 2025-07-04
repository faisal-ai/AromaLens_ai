import os
import re
import json
import requests
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "deepseek-r1-distill-llama-70b"

def extract_json_from_text(text: str) -> dict:

    # extracting JSON from markdown code block
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Fallback: trying to extract the last {...} block in the string
        brace_matches = re.findall(r'(\{.*?\})', text, re.DOTALL)
        if brace_matches:
            json_str = brace_matches[-1]
        else:
            return {"error": "No JSON block found in LLM response."}

    # Parsing the JSON string
    try:
        parsed = json.loads(json_str)
        return parsed
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Raw JSON string:", json_str)
        return {"error": "Invalid JSON in LLM response."}

def query_llm(prompt: str, model: str = GROQ_MODEL) -> dict:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional perfumer assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()

        print("Raw response text:", response.text)

        json_resp = response.json()

        choices = json_resp.get("choices")
        if not choices or len(choices) == 0:
            return {"error": "No choices found in LLM response."}

        message = choices[0].get("message")
        if not message or "content" not in message:
            return {"error": "No message content found in LLM response."}

        content = message["content"]

        # Using updated JSON parser
        result = extract_json_from_text(content)
        return result

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err} - Response text: {response.text}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}
    except ValueError as json_err:
        return {"error": f"JSON decode error: {json_err} - Response text: {response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}