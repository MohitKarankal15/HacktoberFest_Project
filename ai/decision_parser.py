"""
Decision Parser for Gemma 4 Responses
Extracts and parses JSON decisions, stripping code fences and catching malformed output.
"""
import json
import re

def parse_gemma_response(raw_text):
    """
    Parses LLM response string into a structured Python dictionary.
    Returns: (dict or None, error_string or None)
    """
    if not raw_text or not isinstance(raw_text, str):
        return None, "Empty or non-string response received from AI"

    cleaned = raw_text.strip()

    # Case 1: Extract content inside ```json ... ``` or ``` ... ```
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    # Case 2: Attempt direct JSON decode
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data, None
        return None, "Decoded JSON root is not an object/dictionary"
    except json.JSONDecodeError:
        pass

    # Case 3: Search for outermost curly braces { ... }
    brace_match = re.search(r"(\{[\s\S]*\})", cleaned)
    if brace_match:
        try:
            data = json.loads(brace_match.group(1))
            if isinstance(data, dict):
                return data, None
        except json.JSONDecodeError:
            pass

    return None, f"Failed to parse valid JSON from AI response: {raw_text[:100]}..."
