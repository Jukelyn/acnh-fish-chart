# pylint: disable=E0401
"""
This module defines the fish information retrieval routes.
"""
import json
from flask import jsonify, Response

# Load fish data from a JSON file
with open("data/fish_info.json", "r", encoding="utf-8") as file:
    fish_list = {fish["name"].lower(): fish for fish in json.load(file)}


def get_fish_info(fish_name: str) -> Response:
    """
    Returns all specific information about the given fish.

    Args:
        fish_name (str): Fish to be queried.

    Returns:
        (Response): Json representation of the fish data.
    """
    fish_name = fish_name.lower()

    if fish_name in fish_list.keys():
        fish_data = fish_list[fish_name]

        # Return all fish details in a single JSON response
        return jsonify({
            "name": fish_data["name"],
            "image": fish_data["imageURL"],
            "sellPrice": fish_data["sellPrice"],
            "location": fish_data["location"],
            "size": fish_data["size"],
            "time": fish_data["time"],
            "nhMonths": fish_data["nhMonths"],
            "shMonths": fish_data["shMonths"]
        })

    response: Response = jsonify({"error": "Fish not found"})
    response.status_code = 404  # Set status code explicitly
    return response


def fish_info_route(app):
    """
    Registers the /fish-info route.

    This function retrieves fish data based on the fish name provided as a
    query parameter.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.route("/fish-info/<fish_name>", methods=["GET"])
    def wrapped_get_fish_info(fish_name: str):
        return get_fish_info(fish_name)
