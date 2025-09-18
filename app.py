import webview
from backend import api

"""
This is the main entry point for the application.
"""

if __name__ == '__main__':
    # Create an instance of the API class
    api_instance = api.Api()

    # Create a webview window
    webview.create_window(
        'PackLens',
        'web/index.html',
        js_api=api_instance,
        width=800,
        height=600,
        resizable=True,
        fullscreen=False,
        min_size=(400, 300)
    )
    webview.start(debug=True)
