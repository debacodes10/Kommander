import os
from typing import Dict, Any
import google.generativeai as genai

from .context import get_os_info
from .config import load_api_key

def build_prompt(query: str, context: Dict[str, Any]) -> str:
    """Constructs the full prompt to be sent to the AI."""
    
    os_family = context.get("os_family", "system")
    
    prompt = f"""
You are an expert systems administrator for the {os_family} operating system. Your task is to take a user's request and their system context, and generate a concise, safe, and idempotent script to fulfill the request.

- For Windows, generate a PowerShell script.
- For Linux, generate a bash script.
- For Darwin (macOS), generate a zsh/bash script.

The script must be formatted in a single markdown code block. Do not add any explanation outside of the code block.

System Context:
- os_family: {context.get("os_family")}
- architecture: {context.get("architecture")}

User Request: "{query}"

Generate the script:
"""
    return prompt


def call_gemini_api(prompt: str) -> str:
    """Calls the Google Gemini API and returns the generated script."""
    
    api_key = load_api_key()
    if not api_key:
        error_message = (
            "Google API key not found. "
            "Please run 'kom configure' to set your API key."
        )
        return f"Error: {error_message}"
        
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        
        response = model.generate_content(prompt)
        
        if response.parts:
            # --- START OF THE FIX ---
            # 1. Initial cleanup of markdown backticks
            script_text = response.text.strip()
            if script_text.lower().startswith("```powershell"):
                script_text = script_text[13:]
            elif script_text.lower().startswith("```sh"):
                script_text = script_text[5:]
            elif script_text.lower().startswith("```bash"):
                script_text = script_text[7:]
            elif script_text.startswith("```"):
                script_text = script_text[3:]
            
            if script_text.endswith("```"):
                script_text = script_text[:-3]
            
            script_text = script_text.strip()

            # 2. Advanced cleaning for execution hangs
            lines = script_text.splitlines()
            
            # Remove potential language specifier on the first line (e.g., "bash")
            if lines and lines[0].strip().lower() in ["bash", "sh", "zsh", "powershell"]:
                lines.pop(0)

            # Remove potential shebang on the new first line
            if lines and lines[0].strip().startswith("#!"):
                lines.pop(0)

            # 3. Rejoin the clean script
            clean_script = "\n".join(lines).strip()
            
            return clean_script
            # --- END OF THE FIX ---
        else:
            return "Error: Received an empty or blocked response from the API."

    except Exception as e:
        return f"Error calling Google Gemini API: {e}"


def generate_script(query: str) -> str:
    """
    The main orchestration function.
    Takes a user query and returns a generated shell script.
    """
    prompt = build_prompt(query, get_os_info())
    script = call_gemini_api(prompt)
    return script
