from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import logging

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)
STATIC_IMAGES_PATH = 'static/images'

# Load fish data
df = pd.read_csv("data/fish_datasheet.csv")


# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    logging.debug("Handling request to '/' route")
    # List all fish names (for dropdown or filtering)
    all_fishes = df["Name"].dropna().unique().tolist()
    image_url = f"{STATIC_IMAGES_PATH}/NH_spawning_calendar.png"

    if request.method == 'POST':
        logging.debug("Received POST request")
        hemisphere = request.form.get('hemisphere', 'NH')

        filename = f"{STATIC_IMAGES_PATH}/{hemisphere}_spawning_calendar.png"
        image_url = filename

    return render_template('index.html', fish_list=all_fishes,
                           image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
