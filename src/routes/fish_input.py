# pylint: disable=E0401
"""
This module defines the fish input page route.
"""
from flask import render_template


def fish_input_route(app):
    """
    Registers the /fish-input route.

    This function sets up a simple route that serves the fish input page.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.route("/fish-input/")
    def fish_input():
        """
        Serves the fish input page.
        """
        return render_template("fish-input.html")
