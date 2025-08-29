import typer
import subprocess
import pyperclip
import sys
from rich import print
from rich.prompt import Prompt

from .core import generate_script
from .context import get_os_info
from .ui import display_and_confirm_script
from .config import save_api_key # <-- IMPORT a new function

# Create a Typer application instance.
app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Kommander: An AI-powered command-line companion.",
)

@app.command()
def configure():
    """
    Saves your Google AI API key to the configuration file.
    """
    print("[bold yellow]Kommander Configuration[/bold yellow]")
    print("Please enter your Google AI API key. You can get one from Google AI Studio.")
    
    # Use Rich's Prompt for a nice password input
    api_key = Prompt.ask("[bold]API Key[/bold]", password=True)
    
    if not api_key:
        print("[bold red]No API key entered. Configuration cancelled.[/bold red]")
        raise typer.Exit(1)
        
    try:
        save_api_key(api_key)
        print("[bold green]✓ API key saved successfully![/bold green]")
    except Exception as e:
        print(f"[bold red]Failed to save API key: {e}[/bold red]")
        raise typer.Exit(1)

@app.command()
def ask(query: str = typer.Argument(..., help="The task you want to perform.")):
    """
    Asks the AI to generate a script for a given task.
    """
    try:
        print("Calling AI... (This may take a moment)")
        script = generate_script(query)

        if script.lower().startswith("error:"):
            print(f"[bold red]{script}[/bold red]")
            raise typer.Exit(code=1)

        context = get_os_info()
        os_family = context.get("os_family", "Unknown")
        choice = display_and_confirm_script(script, os_family)

        if choice == "execute":
            print("[bold yellow]Executing script...[/bold yellow]")
            
            if sys.platform == "win32":
                command_to_run = ['powershell.exe', '-Command', script]
                use_shell = False
            else:
                command_to_run = script
                use_shell = True

            # --- DEBUGGING PRINTS GO HERE ---

            # [DEBUG 1] Print the command we are about to run
            print(f"\n--- [DEBUG] Command to run ---\n{command_to_run}\n------------------------------") 

            result = subprocess.run(command_to_run, shell=use_shell, check=False, capture_output=True, text=True)
            
            # [DEBUG 2] Print the return code from the process
            print(f"--- [DEBUG] Return Code: {result.returncode}") 
            
            # [DEBUG 3 & 4] Print stdout and stderr, even if they are empty
            print(f"--- [DEBUG] STDOUT ---\n{result.stdout or '(empty)'}\n----------------------")
            print(f"--- [DEBUG] STDERR ---\n{result.stderr or '(empty)'}\n----------------------")

            # --- ORIGINAL CODE CONTINUES ---

            if result.stdout:
                print("[bold green]--- SCRIPT OUTPUT ---[/bold green]")
                print(result.stdout)
            if result.stderr:
                print("[bold red]--- SCRIPT ERROR ---[/bold red]")
                print(result.stderr)
            
            print("[bold green]Execution finished.[/bold green]")

        elif choice == "copy":
            pyperclip.copy(script)
            print("[bold green]Script copied to clipboard![/bold green]")

        elif choice == "abort":
            print("[bold blue]Operation aborted.[/bold blue]")

    except Exception as e:
        print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        raise typer.Exit(code=1)
    
if __name__ == "__main__":
    app()
