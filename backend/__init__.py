from webview import Window

class API:
    '''
    This class defines the API that will be exposed to the frontend.
    '''

    def __init__(self):
        self.window : Window = None
        self.is_maximized = False

    def set_window(self, window):
        self.window = window

    def resize(self, width, height):
        '''
        Resizes the window.
        '''
        if self.window:
            self.window.resize(width, height)

    def minimize(self):
        '''Minimizes the window.'''
        if self.window:
            self.window.minimize()

    def toggle_maximize(self):
        '''Toggles the window's maximized state and updates the flag.'''
        if self.window:
            self.window.toggle_fullscreen()
            self.is_maximized = not self.is_maximized

    def close(self):
        '''Closes the window.'''
        if self.window:
            self.window.destroy()