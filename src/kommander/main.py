import typer
import subprocess
import pyperclip
from rich import print
import sys

from .core import generate_script
from .context import get_os_info
from .ui import display_and_confirm_script

# Typer application instance.
app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Kommander: An AI-powered command-line companion.",
)

@app.command()
def hello(name: str = typer.Argument("World", help="The name to greet.")):
    """
    A simple 'hello world' command to verify the installation.
    """
    print(f"[bold green]Hello, {name}! Kommander is online.[/bold green]")

@app.command()
def check():
    """
    Runs a quick system check and prints the OS info.
    """
    from .context import get_os_info
    
    print("[bold blue]Running system check...[/bold blue]")
    info = get_os_info()
    print(info)

@app.command()
def ask(query: str = typer.Argument(..., help="The task you want to perform.")):
    """
    Asks the AI to generate a script for a given task.
    """
    try:
        # --- 1. GENERATE ---
        script = generate_script(query)

        if script.lower().startswith("error:"):
            print(f"[bold red]{script}[/bold red]")
            raise typer.Exit(code=1)

        # --- 2. CONFIRM ---
        context = get_os_info()
        os_family = context.get("os_family", "Unknown")
        choice = display_and_confirm_script(script, os_family)

        # --- 3. ACT ---
        if choice == "execute":
            print("[bold yellow]Executing script...[/bold yellow]")
            
            # Platform-specific execution logic
            if sys.platform == "win32":
                # On Windows, we explicitly call powershell.exe and pass the script.
                command_to_run = ['powershell.exe', '-Command', script]
                use_shell = False
            else:
                # On Linux/macOS, we run the script string directly with the default shell.
                command_to_run = script
                use_shell = True

            result = subprocess.run(
                command_to_run, 
                shell=use_shell, 
                check=False, 
                capture_output=True, 
                text=True
            )
            
            # Print stdout and stderr from the script
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


# Main entry point
if __name__ == "__main__":
    app()

