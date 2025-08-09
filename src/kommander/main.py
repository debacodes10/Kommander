import typer
from rich import print

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


# Main entry point
if __name__ == "__main__":
    app()

