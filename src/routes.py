# pylint: disable=E0401
"""
This module defines the routes for a Flask web application that handles fish
data input and processing for an Animal Crossing: New Horizons fish chart.

Functions:
    register_routes(app): Registers the routes for the Flask application.
    index(): Handles the root route ("/") for GET and POST requests.
    fish_input(): Renders the fish input form.
    process(): Processes the fish data input from the user and updates the
    fish chart.

Routes:
    / (GET, POST): Renders the main page and handles hemisphere selection.
    /fish-input (GET): Renders the fish input form.
    /process (POST): Processes the fish data input and updates the fish chart.
"""
import logging
from flask import render_template, request, jsonify
import src.utils as ut


def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Routes:
        / (GET, POST): Renders the index page. Handles POST requests to
        update the displayed image based on the selected hemisphere.
        /fish-input (GET): Renders the fish input page.
        /process (POST): Processes the fish input data, filters out
        non-fish items, checks for invalid fish names, and updates the
        fish data. Returns suggestions for invalid fish names if any
        are found, otherwise renders the updated index page.
    """

    @app.route("/", methods=["GET", "POST"])
    def index():
        """
        Handle requests to the root ('/') route.
        Logs the request method and processes POST requests to update the
        current image based on the selected hemisphere. Renders the index
        template with the fish list, uncaught fish, and the current image URL.

        Returns:
            str: Rendered HTML template for the index page.
        """

        logging.debug("Handling request to '/' route")
        if request.method == "POST":
            logging.debug("Received POST request")
            button = request.form.get("hemisphere")
            if button == "NH":
                ut.CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
            elif button == "SH":
                ut.CURRENT_IMAGE = "static/images/SH_spawning_calendar.png"

        return render_template(
            "index.html",
            fish_list=ut.all_fish_list,
            uncaught_fish=ut.uncaught,
            image_url=ut.CURRENT_IMAGE
        )

    @app.route("/fish-input")
    def fish_input():
        """
        Renders the fish input template.
        This function handles the route for the fish input page
        and returns the rendered HTML template for fish input.

        Returns:
            str: Rendered HTML template for fish input.
        """
        return render_template("fish-input.html")

    @app.route("/process", methods=["POST"])
    def process():
        """
        Process the incoming fish data from the request, filter out unwanted
        items, and handle invalid fish names.
        The function performs the following steps:
        1. Decodes the request data.
        2. Cleans and processes the input list of fish names.
        3. Filters out sea creatures, fossils, insects, gyroids, and artwork.
        4. Identifies and logs any invalid fish names.
        5. Provides suggestions for invalid fish names if found.
        6. Processes the valid fish data and renders the result.

        Returns:
            Response: A JSON response with suggestions for invalid fish names
            if any are found, otherwise renders the index.html template with
            the processed fish data.
        """

        data = request.data.decode("utf-8")

        input_list = [fish.strip().replace("_", " ")
                      for fish in data.split("\n") if fish.strip()]

        input_list = [ut.renamed.get(fish, fish)
                      for fish in input_list]

        # I can easily remove art, bugs, fossils, and sea creatures
        # There may be way too many items to check though...
        # Music is kinda a pain to filter as well but I left the logic for it
        # above, ctrl+f for "Music Filtering"
        input_list = ut.filter_data(input_list, ut.sea_creatures)
        input_list = ut.filter_data(input_list, ut.fossils)
        input_list = ut.filter_data(input_list, ut.insects)
        input_list = ut.filter_data(input_list, ut.gyroids)
        input_list = ut.filter_data(input_list, ut.artwork)

        print("\n"*10)
        print(len(input_list))
        print(input_list)
        print("\n"*10)

        problems = ut.get_problems(input_list)
        print("\n"*10)
        print(len(problems))
        print(problems)
        print("\n"*10)
        if problems:
            suggestions = {}
            for prob in problems:
                closest = ut.get_closest_match(prob)
                if closest:
                    suggestions[prob] = closest

            logging.debug("Invalid fish names found: %s", problems)
            logging.debug("Suggested names: %s", suggestions)
            return jsonify({"suggestions": suggestions})

        logging.debug("Fish input saved: %s", input_list)
        # pylint: disable=W0603
        (ut.caught, ut.uncaught, ut.uncaught_NH_df,
         ut.uncaught_SH_df) = ut.process_fish_data(input_list)

        return render_template(
            "index.html",
            fish_list=ut.all_fish_list,
            uncaught_fish=ut.uncaught,
            image_url=ut.CURRENT_IMAGE
        )
