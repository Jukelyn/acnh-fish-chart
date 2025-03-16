# pylint: disable=E0401
"""
This script initializes a Flask application, loads environment variables,
and registers routes.

The script performs the following tasks:
1. Loads environment variables from a .env file using `load_dotenv()`.
2. Creates a Flask application instance with specified template and static
    folders.
3. Configures the Flask application with a secret key from the environment
    variables.
4. Registers application routes using a custom `register_routes` function.

Modules:
     os: Provides a way of using operating system dependent functionality.
     flask: A micro web framework for Python.
     dotenv: Reads key-value pairs from a .env file and can set them as
                environment variables.
     src.routes: A module containing the `register_routes` function to
                     register routes for the Flask app.

Attributes:
     app (Flask): The Flask application instance.
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.routes import register_routes

load_dotenv()

app = Flask(__name__,
            template_folder="../templates",
            static_folder="../static")

# Allow only local dev server
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


register_routes(app)

print("test pylint trigger")
