# pylint: disable=E0401
"""
This module defines the index page.
"""
import logging
import json
from flask import render_template, request
import src.main as ut

# logging.basicConfig(level=logging.DEBUG)


def index_route(app):
    """
    Registers the main entry point of the application.

    This function defines a route that handles both GET and POST requests.
    - On GET requests, it simply renders the main index page.
    - On POST requests, it updates the current image based on the hemisphere.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        (None): This just registers the / route.
    """
    @app.route("/", methods=["GET", "POST"])
    def index():
        """
        Handles requests to the main '/' route.

        If the request method is POST, it checks for a hemisphere selection and
        updates the corresponding spawning calendar image. Then, it renders the
        index page with the available fish data.
        """
        logging.debug("Handling request to '/' route")
        if request.method == "POST":
            logging.debug("Received POST request")
            button = request.form.get("hemisphere")
            if button == "NH":
                ut.CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
            elif button == "SH":
                ut.CURRENT_IMAGE = "static/images/SH_spawning_calendar.png"

        logging.debug("All Fish List: %s", ut.all_fish_list)
        logging.debug("Uncaught Fish List: %s", ut.uncaught)

        return render_template(
            "index.html",
            fish_list=ut.all_fish_list,
            uncaught_fish=ut.uncaught,
            fish_list_json=json.dumps(ut.all_fish_list),
            uncaught_fish_json=json.dumps(sorted(ut.uncaught, key=str.lower)),
            image_url=ut.CURRENT_IMAGE
        )
