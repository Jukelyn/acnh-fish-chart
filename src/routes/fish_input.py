# pylint: disable=E0401
"""
This module provides the route for the fish input page. It handles GET requests
to render the input form and POST requests to process fish data, and can reset
calendars when requested.
"""
import logging
from flask import Flask, render_template, request, jsonify
import src.main as ut


def fish_input_route(app: Flask):
    """
    Register the fish input page route with the Flask app.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        (None): This just registers the /fish-input route.
    """
    @app.route("/fish-input/", methods=["GET", "POST"])
    def fish_input():
        """
        Handle requests for the fish input page.

        - On GET requests, renders the fish input form.
        - On POST requests, processes the input fish data, checks for issues,
          and provides suggestions if necessary. Also supports resetting
          calendars if the input is "reset".

        Returns:
            Response: JSON with status or suggestions on POST, or rendered
                      HTML on GET.
        """
        if request.method == "POST":
            print("POST hit.")
            input_data = request.form.get("fish-data")
            if not input_data:
                input_data = request.get_data(as_text=True)

            if input_data:
                print("Input data received:")
                print(input_data)

                if input_data.strip().lower() == "reset":
                    print("Resetting calendars.")
                    ut.update_calendars()
                    return jsonify({"status": "Calendars reset successfully"})

            input_list = [fish.strip().replace("_", " ").lower()
                          for fish in input_data.split("\n") if fish.strip()]

            input_list = [ut.renamed.get(fish, fish) for fish in input_list]

            problems = ut.get_problems(input_list)
            if problems:
                suggestions: dict[str, list[str]] = {
                    prob: ut.get_closest_match(prob) for prob in problems
                }

                logging.debug("Invalid fish names found: %s", problems)
                logging.debug("Suggested names: %s", suggestions)

                invalid_fish_names: list[str] = list(problems)
                suggestions_list: list[list[str]] = [
                    suggestions[fish] for fish in problems
                ]

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
