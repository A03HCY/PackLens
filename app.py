import webview
import sys
from backend import API
from importlib.metadata import distribution
from server import create_app

'''
This is the main entry point for the application.
'''

def is_frozen():
    '''
    Checks if the application is running as a bundled executable.
    '''
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def debug_mode():
    '''
    Checks if the application is running in debug mode.
    '''
    return not is_frozen()

def check_library(library_name, import_name=None):
    if import_name is None:
        import_name = library_name
    try:
        __import__(import_name)
        return True, "Importable"
    except ImportError:
        try:
            distribution(library_name)
            return False, "Installed but cannot import"
        except ImportError:
            # Fallback for Python < 3.8
            try:
                from pkg_resources import get_distribution
                get_distribution(library_name)
                return False, "Installed but cannot import"
            except:
                return False, "Not installed"
        except Exception:
            return False, "Not installed"

if __name__ == '__main__':
    app = create_app()
    api_instance = API()
    ssl_mode = check_library('cryptography')[0]

    print(f'Debug mode: {debug_mode()}')
    print(f'SSL support: {ssl_mode}')

    # Create a webview window
    window = webview.create_window(
        'PackLens',
        app,
        js_api=api_instance,
        width=800,
        height=600,
        resizable=True,
        fullscreen=False,
        min_size=(400, 300),
        frameless=True,
        easy_drag=False
    )
    api_instance.set_window(window)
    webview.start(debug=debug_mode(), ssl=ssl_mode)
