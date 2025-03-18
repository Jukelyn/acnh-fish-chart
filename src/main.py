# pylint: disable=E0401
"""
This module provides utilities for processing and visualizing data related to
sea creatures, insects, fossils, gyroids, artwork, and fish in the game Animal
Crossing: New Horizons. It includes functions for plotting spawning calendars,
filtering data, and finding the closest matches for user input.

Functions:
    plot_spawning_calendar(dataframe: pd.DataFrame, title: str, filename: str)
        -> None:
            Creates a plot for the fish in a calendar style and saves it as an
            image.

    get_caught_fish(fishes_caught: list[str]) -> list[str]:
        Returns a list of caught fish names based on the input list of fish
        names.

    process_fish_data(input_fish_list: list[str] = None) -> tuple:
        Processes the fish data to separate caught and uncaught fish and
        returns relevant dataframes.

    filter_data(arr: list[str], filter_by: list[str]) -> list[str]:
        Filters the input list by removing items that match the filter list.

    get_closest_match(user_in: str, threshold: int = 80) -> list[str]:
        Finds and returns the closest matches for the user input from the list
        of all fish names.

    get_problems(input_fish: list[str]) -> set[str]:
        Identifies and returns a set of fish names that are not present in the
        list of all fish names.
"""
from datetime import datetime
from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from thefuzz import process as fuzz_process
# from unidecode import unidecode  # For Music Filtering

sea_creatures_df: pd.DataFrame = pd.read_csv(
    "data/sea_creatures_datasheet.csv")
sea_creatures: list[str] = list(sea_creatures_df["Name"].copy())

insects_df: pd.DataFrame = pd.read_csv("data/insects_datasheet.csv")
insects: list[str] = list(insects_df["Name"].copy())

fossils_df: pd.DataFrame = pd.read_csv("data/fossils_datasheet.csv")
fossils: list[str] = list(fossils_df["Name"].copy())

gyroids_df: pd.DataFrame = pd.read_csv("data/gyroids_datasheet.csv")
gyroids: list[str] = list(gyroids_df["Name"].copy())

artwork_df: pd.DataFrame = pd.read_csv("data/artwork_datasheet.csv")
artwork: list[str] = list(set(artwork_df["Name"].copy()))

# Music Filtering
# music: pd.DataFrame = pd.read_csv("data/music_datasheet.csv")
# music: list[str] = list(music["Name"].copy())
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

fish_df = pd.read_csv("data/fish_datasheet.csv")

# Relevant columns for NH_df
NH_columns = ["Name",
              "NH Jan", "NH Feb", "NH Mar",
              "NH Apr", "NH May", "NH Jun",
              "NH Jul", "NH Aug", "NH Sep",
              "NH Oct", "NH Nov", "NH Dec"
              ]
NH_df = fish_df[NH_columns].copy()

# Relevant columns for SH_df
SH_columns = ["Name",
              "SH Jan", "SH Feb", "SH Mar",
              "SH Apr", "SH May", "SH Jun",
              "SH Jul", "SH Aug", "SH Sep",
              "SH Oct", "SH Nov", "SH Dec"
              ]
SH_df = fish_df[SH_columns].copy()

matplotlib.use('Agg')  # no GUI to allow updates from site


def plot_spawning_calendar(
    dataframe: pd.DataFrame, title: str, filename: str
) -> None:
    """
    Creates a plot for the fish in a calendar style and saves it as image.

    Args:
        dataframe (pd.DataFrame): The dataframe with the data for the plot.
        title (str): The title of the plot.
        filename (str): The filename of the saved image.

    Returns:
        (None): This just creates the image files given the fish data.
    """

    plt.figure(figsize=(12, len(dataframe) * 0.5))
    # Convert to 1s and NaNs (1 means spawning, NaN means no spawn)
    spawn_data = dataframe.set_index("Name").notna().astype(int)

    ax = sns.heatmap(spawn_data, cmap="Greens", linewidths=0.5, cbar=False)

    ax.set_xticklabels(["January", "February", "March",
                        "April", "May", "June",
                        "July", "August", "September",
                        "October", "November", "December"
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


def update_calendars(nh_df: pd.DataFrame = NH_df,
                     sh_df: pd.DataFrame = SH_df) -> None:
    """Updates the calendar images based on the fish dataframes.

    Args:
        nh_df (pd.DataFrame): Northern hemisphere fish data.
        sh_df (pd.DataFrame): Southern hemisphere fish data.

    Returns:
        (None): This just calls plot_spawning_calendar() for both hemispheres.
    """

    plot_spawning_calendar(nh_df, "Northern Hemisphere",
                           "NH_spawning_calendar.png")
    plot_spawning_calendar(sh_df, "Southern Hemisphere",
                           "SH_spawning_calendar.png")


update_calendars()

all_fishes: list[str] = sorted(
    list(fish_df["Name"].dropna().unique()), key=str.lower)

CURRENT_IMAGE = "static/images/NH_spawning_calendar.png"
all_fish_list_unsorted: str = fish_df["Name"].dropna().unique().tolist()
all_fish_list: list[str] = sorted(all_fish_list_unsorted, key=str.lower)


def get_caught_fish(fishes_caught: list[str]) -> list[str]:
    """
    Given a list of caught fish names, returns a list of valid fish names that
    have been caught, after filtering for other common items.

    Args:
        fishes_caught (list[str]): A list of strings representing the names of
                                   caught fish.

    Returns:
        (list[str]): Valid fish names that have been caught. If the input list
                     is empty or the first element is empty, returns an empty
                     list.
    """

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

    res = [fish for fish in all_fishes if fish in caught_items]

    return sorted(res, key=str.lower)


def process_fish_data(input_fish_list: Optional[list[str]] = None) -> tuple[
        list[str], list[str], pd.DataFrame, pd.DataFrame]:
    """
    Processes fish data to determine caught and uncaught fish, and returns
    dataframes for uncaught fish in the Northern Hemisphere (NH) and Southern
    Hemisphere (SH).

    Args:
        input_fish_list (list, optional): A list of fish names that have been
                                          caught. Defaults to None.

    Returns:
        (tuple(list, list, pd.Dataframe, pd.Dataframe)):

            - caught_fish (list): Caught fish names.
            - uncaught_fish (list): Uncaught fish names.
            - df_nh_uncaught (DataFrame): Uncaught fish in NH.
            - df_sh_uncaught (DataFrame): Uncaught fish in SH.
    """

    caught_fish = get_caught_fish(input_fish_list or [])
    caught_fish = sorted(caught_fish, key=str.lower)

    uncaught_fish = [fish for fish in all_fishes if fish not in caught_fish]
    uncaught_fish = sorted(uncaught_fish, key=str.lower)

    df_nh_uncaught = NH_df[NH_df["Name"].isin(uncaught_fish)].copy()
    df_sh_uncaught = SH_df[SH_df["Name"].isin(uncaught_fish)].copy()

    update_calendars(df_nh_uncaught, df_sh_uncaught)

    return (caught_fish, uncaught_fish, df_nh_uncaught, df_sh_uncaught)


caught, uncaught, uncaught_NH_df, uncaught_SH_df = process_fish_data()


def filter_data(arr: list[str], filter_by: list[str]) -> list[str]:
    """
    Filters out elements from the input list `arr` that are present in the
    `filter_by` list, ignoring case sensitivity.

    Args:
        arr (list[str]): The list of strings to be filtered.
        filter_by (list[str]): The list of strings to filter out from `arr`.

    Returns:
        (list[str]): A new list with elements from `arr` that are not in
                     `filter_by`, ignoring case.
    """

    arr = [renamed.get(insect, insect)
           for insect in arr]

    filtered_arr = []

    for item in arr:
        if item.lower() not in [thing.lower() for thing in filter_by]:
            filtered_arr.append(item)

    return filtered_arr


def get_closest_match(user_in: str, threshold: int = 80) -> list[str]:
    """
    Finds the closest matching fish names to the user input.
    This function searches for fish names that closely match the
    provided user input string. It uses two methods to find matches:
    1. Direct substring matching.
    2. Fuzzy matching with a specified threshold.

    Args:
        user_in (str): The input string provided by the user to
                       search for matching fish names.
        threshold (int, optional): The minimum score for fuzzy
                                   matching to consider a match.
                                   Defaults to 80.

    Returns:
        (list[str]): Fish names that closely match the user input. The list is
                     determined based on the highest matching scores from
                     either direct substring matching or fuzzy matching.
    """

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
            score for _, score in matches if score >= threshold
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


def get_problems(input_fish: list[str]) -> set[str]:
    """
    Identifies fish names in the input list that are not present in the
    predefined list of all fishes.

    Args:
        input_fish (list[str]): A list of fish names to be checked.

    Returns:
        (set[str]): Fish names that are not found in the predefined
                    list of all fishes.
    """

    return {item for item in input_fish if item not in all_fishes}
