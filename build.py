import PyInstaller.__main__
import os
import shutil
import platform
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# --- Configuration ---
APP_NAME = "PackLens"
MAIN_SCRIPT = "app.py"
VERSION_FILE = "version.txt"
# ---------------------

console = Console()

def cleanup():
    """Removes temporary build files and directories."""
    console.print("[bold yellow]Cleaning up previous build files...[/bold yellow]")
    
    paths_to_remove = ['dist', 'build', f'{APP_NAME}.spec']
    for path in paths_to_remove:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                console.print(f"  [dim]Removed directory:[/] {path}")
            elif os.path.isfile(path):
                os.remove(path)
                console.print(f"  [dim]Removed file:[/] {path}")
        except FileNotFoundError:
            pass # Ignore if path doesn't exist
    console.print("[green]Cleanup complete.[/green]\n")

def build():
    """Runs the PyInstaller build process."""
    pyinstaller_args = [
        MAIN_SCRIPT,
        f'--name={APP_NAME}',
        '--onefile',
        '--windowed',
        f'--version-file={VERSION_FILE}',
        '--add-data=backend;backend',
        '--add-data=web;web',
    ]

    console.print(Panel.fit(
        f"[bold cyan]Starting PyInstaller for {APP_NAME}[/bold cyan]",
        title="Build Process"
    ))
    
    console.print("PyInstaller arguments:", style="dim")
    console.print(f"  {' '.join(pyinstaller_args)}\n", style="dim")

    try:
        PyInstaller.__main__.run(pyinstaller_args)
        console.print("\n[bold green]PyInstaller finished successfully.[/bold green]")
        return True
    except Exception as e:
        console.print(f"\n[bold red]An error occurred during the build process:[/bold red]")
        console.print_exception()
        return False

def post_build_cleanup():
    """Cleans up artifacts left after the build."""
    console.print("\n[bold yellow]Cleaning up post-build artifacts...[/bold yellow]")
    if os.path.isdir('build'):
        shutil.rmtree('build')
        console.print("  [dim]Removed directory:[/] build")
    if os.path.isfile(f'{APP_NAME}.spec'):
        os.remove(f'{APP_NAME}.spec')
        console.print(f"  [dim]Removed file:[/] {APP_NAME}.spec")
    console.print("[green]Post-build cleanup complete.[/green]")

def get_file_size(path):
    """Returns the size of a file in a human-readable format."""
    size_bytes = os.path.getsize(path)
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.2f} KB"
    else:
        return f"{size_bytes/1024**2:.2f} MB"

def display_summary():
    """Displays a summary of the build output."""
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    executable_path = os.path.join('dist', f'{APP_NAME}{exe_ext}')

    if not os.path.exists(executable_path):
        console.print(f"\n[bold red]Build failed: Executable not found at {executable_path}[/bold red]")
        return

    file_size = get_file_size(executable_path)
    
    summary_text = Text.assemble(
        ("Application: ", "bold"), (f"{APP_NAME}\n"),
        ("Platform: ", "bold"), (f"{platform.system()} {platform.machine()}\n"),
        ("Version Info: ", "bold"), (f"Embedded from {VERSION_FILE}\n"),
        ("Location: ", "bold"), (f"{os.path.abspath(executable_path)}\n", "cyan"),
        ("Size: ", "bold"), (f"{file_size}", "magenta")
    )

    console.print(Panel(
        summary_text,
        title="[bold green]Build Successful[/bold green]",
        expand=False,
        border_style="green"
    ))

if __name__ == '__main__':
    cleanup()
    if build():
        post_build_cleanup()
        display_summary()
    else:
        console.print("\n[bold red]Build process failed. Please check the output above for errors.[/bold red]")
