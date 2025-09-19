import PyInstaller.__main__
import os
import shutil
import platform
try:
    import tomllib
except ImportError:
    import toml as tomllib
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# --- Load Configuration ---
with open('build.toml', 'rb') as f:
    config = tomllib.load(f)

# App Config
app_config = config.get('app', {})
APP_NAME = app_config.get('app_name')
MAIN_SCRIPT = app_config.get('main_script')
INCLUDE_SSL = app_config.get('include_ssl', True)
VERSION_FILE = "version.txt" # This is temporary

# Version Config
version_config = config.get('version', {})
VERSION = version_config.get('version')
COMPANY_NAME = version_config.get('company_name')
FILE_DESCRIPTION = version_config.get('file_description')
INTERNAL_NAME = version_config.get('internal_name')
PRODUCT_NAME = version_config.get('product_name')
LEGAL_COPYRIGHT = f"© {datetime.now().year} {COMPANY_NAME}. All rights reserved."
ORIGINAL_FILENAME = f"{APP_NAME}.exe"
# ---------------------------

console = Console()

def create_version_file():
    """Generates the version.txt file from configuration."""
    console.print(f"[bold yellow]Generating {VERSION_FILE}...[/bold yellow]")
    
    major, minor, patch, build_num = VERSION.split('.')
    
    version_info_content = f"""
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major}, {minor}, {patch}, {build_num}),
    prodvers=({major}, {minor}, {patch}, {build_num}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{COMPANY_NAME}'),
        StringStruct(u'FileDescription', u'{FILE_DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{VERSION}'),
        StringStruct(u'InternalName', u'{INTERNAL_NAME}'),
        StringStruct(u'LegalCopyright', u'{LEGAL_COPYRIGHT}'),
        StringStruct(u'OriginalFilename', u'{ORIGINAL_FILENAME}'),
        StringStruct(u'ProductName', u'{PRODUCT_NAME}'),
        StringStruct(u'ProductVersion', u'{VERSION}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(version_info_content)
    console.print(f"[green]{VERSION_FILE} generated successfully.[/green]\n")

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

    # Exclude PyQt/PySide on Windows, as EdgeChromium is used
    if platform.system() == "Windows":
        qt_modules_to_exclude = ['PyQt5', 'PyQt6', 'PySide2', 'PySide6']
        for module in qt_modules_to_exclude:
            pyinstaller_args.append(f'--exclude-module={module}')
            
    # Exclude cryptography if SSL is not included
    if not INCLUDE_SSL:
        pyinstaller_args.append('--exclude-module=cryptography')
        console.print("[bold yellow]SSL support is disabled. Excluding 'cryptography' module.[/bold yellow]")

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
    paths_to_remove = [
        'build', 
        f'{APP_NAME}.spec',
        VERSION_FILE
    ]
    
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
    create_version_file()
    if build():
        post_build_cleanup()
        display_summary()
    else:
        console.print("\n[bold red]Build process failed. Please check the output above for errors.[/bold red]")
