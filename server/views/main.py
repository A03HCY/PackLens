from flask import Blueprint, render_template, request, jsonify
from functools import wraps
import webview
import json

bp = Blueprint('main', __name__)

def verify_token(function):
    """Decorator to verify the webview token for API security."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            data = json.loads(request.data)
            token = data.get('token')
        except (json.JSONDecodeError, AttributeError):
            token = None
            
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            # Return a 401 Unauthorized error
            return jsonify({'error': 'Authentication error'}), 401
    return wrapper


@bp.route('/')
def index():
    """Serve the main HTML file, passing the security token to the template."""
    return render_template('frame.html')