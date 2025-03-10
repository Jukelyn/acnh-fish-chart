# pylint: disable=E0401, C0114, C0116
import logging
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)

# Load fish data
df = pd.read_csv("data/fish_datasheet.csv")

CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"


# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    logging.debug("Handling request to '/' route")
    # List all fish names (for dropdown or filtering)
    all_fishes = df["Name"].dropna().unique().tolist()

    global CURRENT_IMAGE  # pylint: disable=W0603
    if request.method == 'POST':
        logging.debug("Received POST request")
        button = request.form.get("hemisphere")
        if button == "NH":
            CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
        elif button == "SH":
            CURRENT_IMAGE = "static/images/SH_spawning_calendar.png"

    return render_template('index.html', fish_list=all_fishes,
                           image_url=CURRENT_IMAGE)


if __name__ == '__main__':
    app.run(debug=True)
