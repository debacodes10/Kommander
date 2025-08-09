import os
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

from .context import get_os_info

# Load environment variables from .env file
load_dotenv()

def build_prompt(query: str, context: Dict[str, Any]) -> str:
    """Constructs the full prompt to be sent to the AI."""
    
    os_family = context.get("os_family", "system") # Default to 'system' if not found
    
    # This prompt is now dynamic based on the detected OS family.
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
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not found.")
        
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        
        response = model.generate_content(prompt)
        
        if response.parts:
            # Clean up the output to remove the markdown backticks
            script_text = response.text.strip()
            if script_text.lower().startswith("```powershell"):
                script_text = script_text[13:]
            elif script_text.lower().startswith("```sh"):
                script_text = script_text[5:]
            elif script_text.startswith("```"):
                script_text = script_text[3:]
            
            if script_text.endswith("```"):
                script_text = script_text[:-3]
            
            return script_text.strip()
        else:
            return "Error: Received an empty or blocked response from the API."

    except Exception as e:
        return f"Error calling Google Gemini API: {e}"


def generate_script(query: str) -> str:
    """
    The main orchestration function.
    Takes a user query and returns a generated shell script.
    """
    print("Gathering system context...")
    context = get_os_info()
    
    print("Building OS-specific prompt for Gemini...")
    prompt = build_prompt(query, context)
    
    print("Calling Gemini AI... (This may take a moment)")
    script = call_gemini_api(prompt)
    
    return script