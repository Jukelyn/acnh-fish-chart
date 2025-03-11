# pylint: disable=E0401, C0114, C0116
import logging
from datetime import datetime
from thefuzz import process as fuzz_process
from flask import Flask, render_template, request, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
# from unidecode import unidecode  # For Music Filtering

app = Flask(__name__, static_folder="static")

logging.basicConfig(level=logging.DEBUG)

# Load fish data
df = pd.read_csv("data/fish_datasheet.csv")


# Relevant columns for NH_df
NH_columns = [
    "Name",
    "NH Jan",
    "NH Feb",
    "NH Mar",
    "NH Apr",
    "NH May",
    "NH Jun",
    "NH Jul",
    "NH Aug",
    "NH Sep",
    "NH Oct",
    "NH Nov",
    "NH Dec"
]
NH_df = df[NH_columns].copy()

# Relevant columns for SH_df
SH_columns = [
    "Name",
    "SH Jan",
    "SH Feb",
    "SH Mar",
    "SH Apr",
    "SH May",
    "SH Jun",
    "SH Jul",
    "SH Aug",
    "SH Sep",
    "SH Oct",
    "SH Nov",
    "SH Dec"
]
SH_df = df[SH_columns].copy()


def plot_spawning_calendar(
    dataframe: pd.DataFrame, title: str, filename: str
) -> None:
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

    ax.set_xticklabels(
        ["January",
         "February",
         "March",
         "April",
         "May",
         "June",
         "July",
         "August",
         "September",
         "October",
         "November",
         "December"
         ]
    )

    plt.xlabel("")
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")

    # Add a red line between the columns of the current month
    current_month = datetime.now().month
    ax.axvline(x=current_month - 0.5, color="red", linestyle="-", linewidth=2)
    # Create a custom legend
    legend_elements = [
        Line2D([0], [0], color="red", lw=2, label="Current Month")]
    ax.legend(handles=legend_elements,
              loc="upper right", bbox_to_anchor=(1.2, 1))

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

renamed: dict[str, str] = {  # Dict of items that need to be renamed
    "citrus long horned beetle": "citrus long-horned beetle",
    "earth boring dung beetle": "earth-boring dung beetle",
    "man faced stink bug": "man-faced stink bug",
    "shark tooth pattern": "shark-tooth pattern",
    "queen alexandras birdwing": "Queen Alexandra's birdwing",
    "rajah brookes birdwing": "Rajah Brooke's birdwing",
    "t rex skull": "T. rex skull",
    "t rex tail": "T. rex tail",
    "t rex torso": "T. rex torso",
    "rock head statue": "rock-head statue",
    "pop eyed goldfish": "pop-eyed goldfish",
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
        fish_name = fishy.strip().replace("_", " ")
        fish_name = renamed.get(fish_name, fish_name)

        caught_items.add(fish_name)

    return [fish for fish in all_fishes if fish in caught_items]


def process_fish_data(input_fish_list=None):
    caught_fish = get_caught_fish(input_fish_list or [])
    uncaught_fish = [fish for fish in all_fishes if fish not in caught_fish]
    df_nh_uncaught = NH_df[NH_df["Name"].isin(uncaught_fish)].copy()
    df_sh_uncaught = SH_df[SH_df["Name"].isin(uncaught_fish)].copy()
    return caught_fish, uncaught_fish, df_nh_uncaught, df_sh_uncaught


caught, uncaught, uncaught_NH_df, uncaught_SH_df = process_fish_data()

CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
all_fish_list = df["Name"].dropna().unique().tolist()


@app.route("/", methods=["GET", "POST"])
def index():
    logging.debug("Handling request to '/' route")
    global CURRENT_IMAGE  # pylint: disable=W0603
    if request.method == "POST":
        logging.debug("Received POST request")
        button = request.form.get("hemisphere")
        if button == "NH":
            CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
        elif button == "SH":
            CURRENT_IMAGE = "static/images/SH_spawning_calendar.png"

    return render_template(
        "index.html",
        fish_list=all_fish_list,
        uncaught_fish=uncaught,
        image_url=CURRENT_IMAGE
    )


def get_closest_match(user_in: str, threshold: int = 80):
    possible_matches = [
        fish for fish in all_fishes if user_in.lower() in fish.lower()
    ]

    if possible_matches:
        possible_matches_scores = [
            fuzz_process.extractOne(user_in, [fish])[1]
            for fish in possible_matches
        ]
        possible_matches_max_score = max(possible_matches_scores)
    else:
        possible_matches_max_score = 0

    matches = fuzz_process.extract(user_in, all_fishes, limit=len(all_fishes))
    filtered_matches = [match for match,
                        score in matches if score >= threshold]

    if filtered_matches:
        filtered_matches_scores = [
            score for match, score in matches if score >= threshold
        ]
        filtered_matches_max_score = max(filtered_matches_scores)
    else:
        filtered_matches_max_score = 0

    if possible_matches_max_score > filtered_matches_max_score:
        return possible_matches

    if filtered_matches_max_score > possible_matches_max_score:
        return filtered_matches

    if len(possible_matches) >= len(filtered_matches):
        return possible_matches

    return filtered_matches


sea_creatures = pd.read_csv("data/sea_creatures_datasheet.csv")
sea_creatures = list(sea_creatures["Name"].copy())

insects = pd.read_csv("data/insects_datasheet.csv")
insects = list(insects["Name"].copy())

fossils = pd.read_csv("data/fossils_datasheet.csv")
fossils = list(fossils["Name"].copy())

gyroids = pd.read_csv("data/gyroids_datasheet.csv")
gyroids = list(gyroids["Name"].copy())

artwork = pd.read_csv("data/artwork_datasheet.csv")
artwork = list(set(artwork["Name"].copy()))

# Music Filtering
# music = pd.read_csv("data/music_datasheet.csv")
# music = list(music["Name"].copy())
# find_these_songs = [
#     'cafe_kk',
#     'kk_etude',
#     'lucky_kk',
#     'kk_stroll',
#     'kk_synth',
#     'surfin_kk',
#     'rockin_kk',
#     'kk_cruisin',
#     'drivin'
# ]
# find_these_songs = [item.replace('_', ' ').replace(
#     'kk', 'k.k.') for item in find_these_songs]
# music = [unidecode(song.lower()).replace("'", "") for song in music]
# found = []
# for song in find_these_songs:
#     if song in music:
#         found.append(song)

# print(len(found) == len(find_these_songs))  # True


def filter_stuff(arr: list[str], filter_by: list[str]) -> list[str]:
    arr = [renamed.get(insect, insect)
           for insect in arr]

    filtered_arr = []

    for item in arr:
        if item.lower() not in [thing.lower() for thing in filter_by]:
            filtered_arr.append(item)

    return filtered_arr


def get_problems(input_fish: list[str]) -> set[str]:
    problem_children = set()

    for item in input_fish:
        if item not in all_fishes:
            problem_children.add(item)

    return problem_children


@app.route("/fish-input")
def fish_input():
    return render_template("fish-input.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.data.decode("utf-8")

    input_list = [fish.strip().replace("_", " ")
                  for fish in data.split("\n") if fish.strip()]

    input_list = [renamed.get(fish, fish)
                  for fish in input_list]

    # I can easily remove art, bugs, fossils, and sea creatures
    # There may be way too many items to check though...
    # Music is kinda a pain to filter as well but I left the logic for it
    # above, ctrl+f for "Music Filtering"
    input_list = filter_stuff(input_list, sea_creatures)
    input_list = filter_stuff(input_list, fossils)
    input_list = filter_stuff(input_list, insects)
    input_list = filter_stuff(input_list, gyroids)
    input_list = filter_stuff(input_list, artwork)

    print("\n"*10)
    print(len(input_list))
    print(input_list)
    print("\n"*10)

    problems = get_problems(input_list)
    print("\n"*10)
    print(len(problems))
    print(problems)
    print("\n"*10)
    if problems:
        suggestions = {}
        for prob in problems:
            closest = get_closest_match(prob)
            if closest:
                suggestions[prob] = closest

        logging.debug("Invalid fish names found: %s", problems)
        logging.debug("Suggested names: %s", suggestions)
        return jsonify({"suggestions": suggestions})

    logging.debug("Fish input saved: %s", input_list)
    # pylint: disable=W0603
    global caught, uncaught, uncaught_NH_df, uncaught_SH_df
    caught, uncaught, uncaught_NH_df, uncaught_SH_df = process_fish_data(
        input_list)

    return render_template(
        "index.html",
        fish_list=all_fish_list,
        uncaught_fish=uncaught,
        image_url=CURRENT_IMAGE
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
