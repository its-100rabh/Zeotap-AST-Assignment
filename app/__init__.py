# This file defines the Flask application factory.
# 1. Initializes the Flask app.
# 2. Sets up the API routes by importing and initializing them.

from flask import Flask

def create_app():
    app = Flask(__name__)

    from . import api
    api.init_app(app)

    return app
