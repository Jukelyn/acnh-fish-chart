# pylint: disable=E0401
"""
This module defines and handles all of the processing for the fish input data.
"""
import logging
from flask import render_template, request, jsonify
import src.main as ut


def process_route(app):
    """
    Registers the process route for processing fish-related data.

    This function sets up a Flask route that handles POST requests containing a
    list of fish names. The names are processed, filtered, and validated
    against known categories such as sea creatures, fossils, insects, gyroids,
    and artwork. If any names are invalid, suggestions for corrections are
    provided. The processed data is then used to determine which fish have been
    caught or remain uncaught.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.route("/process/", methods=["POST"])
    def process():
        """
        Handles the processing of fish names submitted via POST request.

        Flow:
        1. Decode and clean the input list.
        2. Replace fish names based on predefined mappings, if needed.
        3. Filter out non-relevant entries.
        4. Identify and suggest corrections for invalid fish names.
        5. Process the valid fish list and updates caught/uncaught fish lists.

        Returns:
            Response:
                - JSON response with suggestions if invalid names are found.
                - Renders the 'index.html' template with updated fish data.
        """
        data = request.data.decode("utf-8")

        input_list = [fish.strip().replace("_", " ")
                      for fish in data.split("\n") if fish.strip()]

        input_list = [ut.renamed.get(fish, fish)
                      for fish in input_list]

        problems = ut.get_problems(input_list)
        if problems:
            suggestions = {prob: ut.get_closest_match(
                prob) for prob in problems}
            logging.debug("Invalid fish names found: %s", problems)
            logging.debug("Suggested names: %s", suggestions)
            invalid_fish_names = list(problems)
            suggestions_list = [suggestions[fish] for fish in problems]
            return jsonify({
                "invalid_fish_names": invalid_fish_names,
                "suggestions": suggestions_list
            })

        logging.debug("Fish input saved: %s", input_list)
        (ut.caught, ut.uncaught, ut.uncaught_NH_df,
         ut.uncaught_SH_df) = ut.process_fish_data(input_list)

        return render_template(
            "index.html",
            fish_list=ut.all_fish_list,
            uncaught_fish=ut.uncaught,
            image_url=ut.CURRENT_IMAGE
        )
