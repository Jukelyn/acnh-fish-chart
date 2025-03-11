# pylint: disable=E0401, C0114, C0116
import logging
from datetime import datetime
from thefuzz import process as fuzz_process
from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)

# Load fish data
df = pd.read_csv("data/fish_datasheet.csv")

# Relevant columns for NH_df
NH_columns = ["Name", "NH Jan", "NH Feb", "NH Mar", "NH Apr", "NH May",
              "NH Jun", "NH Jul", "NH Aug", "NH Sep", "NH Oct", "NH Nov",
              "NH Dec"]
NH_df = df[NH_columns].copy()

# Relevant columns for SH_df
SH_columns = ["Name", "SH Jan", "SH Feb", "SH Mar", "SH Apr", "SH May",
              "SH Jun", "SH Jul", "SH Aug", "SH Sep", "SH Oct", "SH Nov",
              "SH Dec"]
SH_df = df[SH_columns].copy()


def plot_spawning_calendar(dataframe: pd.DataFrame, title: str,
                           filename: str) -> None:
    """Creates a plot for the fish in a calendar style and saves it as image.

    Args:
        dataframe (pd.DataFrame): The dataframe with the data for the plot.
        title (str): The title of the plot.
        filename (str): The filename of the saved image.
    """

    plt.figure(figsize=(12, len(dataframe) * 0.5))
    # Convert to 1s and NaNs (1 means spawning, NaN means no spawn)
    spawn_data = dataframe.set_index("Name").notna().astype(int)

    ax = sns.heatmap(spawn_data, cmap="Greens", linewidths=0.5, cbar=False)

    ax.set_xticklabels(["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November",
                        "December"])

    plt.xlabel("")
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")

    # Add a red line between the columns of the current month
    current_month = datetime.now().month
    ax.axvline(x=current_month - 0.5, color='red', linestyle='-', linewidth=2)
    # Create a custom legend
    legend_elements = [
        Line2D([0], [0], color='red', lw=2, label='Current Month')]
    ax.legend(handles=legend_elements,
              loc='upper right', bbox_to_anchor=(1.2, 1))

    plt.ylabel("")
    plt.title(title, loc="center")
    plt.xticks(rotation=45)
    plt.yticks()

    plt.savefig("static/images/" + filename, bbox_inches="tight", dpi=300)
    # plt.show()

    plt.close()


plot_spawning_calendar(NH_df, "Northern Hemisphere",
                       "NH_spawning_calendar.png")
plot_spawning_calendar(SH_df, "Southern Hemisphere",
                       "SH_spawning_calendar.png")
all_fishes: list[str] = list(df["Name"].dropna().unique())
renamed_fish: dict[str, str] = {"pop eyed goldfish": "pop-eyed goldfish",
                                "soft shelled turtle": "soft-shelled turtle",
                                "napoleonfish": "Napoleonfish",
                                "mahi mahi": "mahi-mahi"
                                }


# Change this to get inputs from browser instead
def get_caught_fish(fishes_caught: list[str]) -> list[str]:
    try:
        if not fishes_caught[0]:
            return []
    except IndexError:
        return []

    caught_items = set()

    for fishy in fishes_caught:
        fish_name = fishy.strip().replace('_', ' ')
        fish_name = renamed_fish.get(fish_name, fish_name)

        caught_items.add(fish_name)

    return [fish for fish in all_fishes if fish in caught_items]


caught_fish = get_caught_fish([])
uncaught_fish = [fish for fish in all_fishes if fish not in caught_fish]
uncaught_NH_df = NH_df[NH_df['Name'].isin(uncaught_fish)].copy()
uncaught_SH_df = SH_df[SH_df['Name'].isin(uncaught_fish)].copy()

CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
all_fish_list = df["Name"].dropna().unique().tolist()


@app.route('/', methods=['GET', 'POST'])
def index():
    logging.debug("Handling request to '/' route")
    global CURRENT_IMAGE  # pylint: disable=W0603
    if request.method == 'POST':
        logging.debug("Received POST request")
        button = request.form.get("hemisphere")
        if button == "NH":
            CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
        elif button == "SH":
            CURRENT_IMAGE = "static/images/SH_spawning_calendar.png"

    return render_template('index.html', fish_list=all_fish_list,
                           uncaught_fish=uncaught_fish,
                           image_url=CURRENT_IMAGE)


@app.route('/fish-input')
def fish_input():
    return render_template('fish-input.html')


def get_closest_match(user_in: str, threshold: int = 80):
    possible_matches = [
        fish for fish in all_fishes if user_in.lower() in fish.lower()]

    if not possible_matches:
        return None

    matches = fuzz_process.extract(user_in, all_fishes, limit=len(all_fishes))
    filtered_matches = [match for match,
                        score in matches if score >= threshold]

    return filtered_matches if filtered_matches else None


def get_problems(input_fish: list[str]) -> set[str]:
    problem_children = set()

    for item in input_fish:
        if item not in all_fishes:
            problem_children.add(item)

    return problem_children


@app.route('/process', methods=['POST'])
def process():
    data = request.data.decode("utf-8")  # Get raw text

    # Convert to list, remove empty lines
    input_fish_list = [fish.strip()
                       for fish in data.split("\n") if fish.strip()]

    problems = get_problems(input_fish_list)

    if problems:
        suggestions = {}
        print(f"{problems} fishes are not valid.")
        for prob in problems:
            closest = get_closest_match(prob)

            if closest is None:
                suggestions[prob] = None
            else:
                suggestions[prob] = closest

        print(f"Suggested names: {suggestions}")

    logging.debug("Fish input saved: %s", input_fish_list)
    # pylint: disable=W0603
    global caught_fish, uncaught_fish, uncaught_NH_df, uncaught_SH_df
    caught_fish = get_caught_fish(input_fish_list)

    uncaught_fish = [fish for fish in all_fishes if fish not in caught_fish]
    uncaught_NH_df = NH_df[NH_df['Name'].isin(uncaught_fish)].copy()
    uncaught_SH_df = SH_df[SH_df['Name'].isin(uncaught_fish)].copy()

    # logging.debug("All fish list: %s", all_fish_list)
    return render_template('index.html', fish_list=all_fish_list,
                           uncaught_fish=uncaught_fish,
                           image_url=CURRENT_IMAGE)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
