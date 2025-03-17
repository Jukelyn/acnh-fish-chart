# pylint: disable=E0401
"""
This module defines the fish input page route.
"""
import logging
from flask import render_template, request, jsonify
import src.main as ut


def fish_input_route(app):
    """
    Registers the /fish-input route.

    This function sets up a simple route that serves the fish input page.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.route("/fish-input/", methods=["GET", "POST"])
    def fish_input():
        """
        Serves the fish input page.
        """

        if request.method == "POST":
            print("POST hit.")
            input_data = request.form.get("fish-data")
            if not input_data:
                input_data = request.get_data(as_text=True)

            if input_data:
                print("Input data received:")
                print(input_data)

            input_list = [fish.strip().replace("_", " ").lower()
                          for fish in input_data.split("\n") if fish.strip()]

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

        return render_template("fish-input.html")
