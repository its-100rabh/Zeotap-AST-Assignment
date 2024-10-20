# This file initializes and runs the Flask application.
# 1. 'create_app()' - Initializes the Flask app with configurations and routes.
# 2. The app runs in debug mode when executed directly.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
