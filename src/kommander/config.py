import os
from pathlib import Path
import configparser

# Define the path for our configuration directory
# This will be ~/.kommander on Linux/macOS and C:\Users\YourUser\.kommander on Windows
CONFIG_DIR = Path.home() / ".kommander"
CONFIG_FILE = CONFIG_DIR / "config.ini"

def save_api_key(api_key: str):
    """Saves the Google API key to the config file."""
    try:
        # Ensure the configuration directory exists
        CONFIG_DIR.mkdir(exist_ok=True)
        
        config = configparser.ConfigParser()
        config["API"] = {"google_api_key": api_key}
        
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
            
    except Exception as e:
        # In a real app, you might want more specific error handling
        print(f"Error saving configuration: {e}")
        raise

def load_api_key() -> str | None:
    """Loads the Google API key from the config file."""
    if not CONFIG_FILE.is_file():
        return None
        
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config.get("API", "google_api_key", fallback=None)
    except (configparser.Error, IOError):
        return None

