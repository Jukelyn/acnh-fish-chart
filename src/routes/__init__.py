"""
This module intiates the routes for the application.

Functions:
    register_routes(app): Registers the routes for the Flask application.
    index_route(): Handles the root route ("/") for GET and POST requests.
    fish_input_route(): Renders the fish input form.
    process_route(): Processes the fish data input from the user and updates
    the fish calendar.
"""
from .index import index_route
from .fish_input import fish_input_route
from .process import process_route


def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Routes:
        routes.index: Renders the main page and handles hemisphere selection.
        routes.fish_input: Renders the fish input form.
        routes.process: Processes the fish data input and updates the calendar.
    """
    index_route(app)
    fish_input_route(app)
    process_route(app)
