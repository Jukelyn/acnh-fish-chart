import logging
from flask import render_template, request, jsonify
from flask_socketio import SocketIO, emit
import src.main as ut


def fish_input_route(app, socketio):
    """
    Registers the /fish-input route and WebSocket communication.

    This function sets up a simple route that serves the fish input page and
    handles WebSocket communication.
    """
    socketio.init_app(app)

    @app.route("/fish-input/", methods=["GET", "POST"])
    def fish_input():
        """
        Serves the fish input page.
        """
        if request.method == "POST":
            # Existing POST code for handling the form submission (unchanged)
            data = request.data.decode("utf-8")

            input_list = [fish.strip().replace("_", " ").lower()
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

        return render_template("fish-input.html")

    @socketio.on('send_fish_data')
    def handle_fish_data(data):
        """
        Handle the WebSocket message containing fish data.
        """
        logging.debug("Received data from JS: %s", data)

        input_list = [fish.strip().replace("_", " ").lower()
                      for fish in data.split("\n") if fish.strip()]
        input_list = [ut.renamed.get(fish, fish) for fish in input_list]

        problems = ut.get_problems(input_list)
        if problems:
            suggestions = {prob: ut.get_closest_match(
                prob) for prob in problems}
            logging.debug("Invalid fish names found: %s", problems)
            logging.debug("Suggested names: %s", suggestions)
            invalid_fish_names = list(problems)
            suggestions_list = [suggestions[fish] for fish in problems]
            emit('receive_suggestions', {
                'invalid_fish_names': invalid_fish_names,
                'suggestions': suggestions_list
            })
        else:
            logging.debug("Fish input saved: %s", input_list)
            (ut.caught, ut.uncaught, ut.uncaught_NH_df,
             ut.uncaught_SH_df) = ut.process_fish_data(input_list)
            emit('fish_data_processed', {
                'uncaught_fish': ut.uncaught,
                'image_url': ut.CURRENT_IMAGE
            })
