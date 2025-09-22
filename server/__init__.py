from flask import Flask
import os

def create_app():
    """Create and configure an instance of the Flask application."""
    
    web_dir = os.path.join(os.path.dirname(__file__), '..', 'web')

    app = Flask(__name__, static_folder=web_dir, template_folder=web_dir)

    # Disable caching for development
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
    app.config['SECRET_KEY'] = 'secret' # It's important to set a secret key for session management

    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    # Register blueprints
    from .views import main
    app.register_blueprint(main.bp)

    return app
