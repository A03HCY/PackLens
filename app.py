import webview
import sys
from backend import api

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

if __name__ == '__main__':
    # Create an instance of the API class
    api_instance = api.API()

    print(f'Debug mode: {debug_mode()}')

    # Create a webview window
    window = webview.create_window(
        'PackLens',
        'web/index.html',
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
    webview.start(debug=debug_mode())
