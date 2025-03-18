# pylint: disable=E0401
"""
This module provides the route for the export page. It handles GET requests to
display fish data, including all available fish and uncaught fish.
"""
import logging
import json
from flask import render_template
import src.main as ut

# logging.basicConfig(level=logging.DEBUG)


def export_route(app):
    """
    Register the export page route with the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.route("/export")
    def export():
        """
        Handles requests to the '/export' route.
        """
        logging.debug("Handling request to 'export' route")
        return render_template(
            "export.html",
            fish_list=ut.all_fish_list,
            uncaught_fish=ut.uncaught,
            fish_list_json=json.dumps(ut.all_fish_list),
            uncaught_fish_json=json.dumps(sorted(ut.uncaught, key=str.lower))
        )
