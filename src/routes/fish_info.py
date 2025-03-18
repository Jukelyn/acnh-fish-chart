# pylint: disable=E0401
"""
This module provides routes and functions for retrieving detailed fish
information from a JSON data source.
"""
import json
from flask import Flask, jsonify, Response

# Load fish data from a JSON file
with open("data/fish_info.json", "r", encoding="utf-8") as file:
    fish_list = {fish["name"].lower(): fish for fish in json.load(file)}


def get_fish_info(fish_name: str):
    """
    Retrieve information about a specific fish by its name.

    Args:
        fish_name (str): The name of the fish to retrieve information for.

    Returns:
        (Response): A JSON response containing fish details if found, otherwise
                  a 404 error with an error message.
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


def fish_info_route(app: Flask):
    """
    Register the fish information retrieval route with the Flask app.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        (None): This just registers the /fish-info route.
    """
    @app.route("/fish-info/<fish_name>", methods=["GET"])
    def wrapped_get_fish_info(fish_name: str):
        """
        Handle GET requests to retrieve fish information by name.

        Args:
            fish_name (str): The name of the fish to retrieve information for.

        Returns:
            Response: JSON response with fish details or an error message.
        """
        return get_fish_info(fish_name)
