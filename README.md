# ACNH Fish Guide
This program processes fish spawning data from a CSV file and provides a visual representation of when different fish spawn throughout the year. It also tracks caught fish from a separate text file and this will be used to suggest optimal months to fish during to maximize the odds of catching new fish.

## Current Features:
1. **Reads fish spawning data** from `data/fish_datasheet.csv`, extracting all fish names and their spawning months.
2. **Creates two DataFrames:**
   - `NH_df` → Contains fish names and their **Northern Hemisphere** spawning months.
   - `SH_df` → Contains fish names and their **Southern Hemisphere** spawning months.
3. **Generates spawning calendar heatmaps** for both hemispheres:
   - Rows: Fish names
   - Columns: Months (January–December)
   - Colored cells: Indicate spawning months
   - Displays the charts in **Jupyter Notebook** and saves them as high-quality `.png` images.
4. **Reads the `data/caught.txt` file**, identifying which fish have been caught:
   - Extracts the names of caught fish from the text file.
   - Compares them to the list of all fish from the CSV.
   - Saves caught fish in a new array called `caught_fish`.

## Information
The fish spawning data is from [this spreadsheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vTGrIfAI5ybCvaiIux5kEbermRFZe6aooAs7I1iVrJF27DrXSOJQxxEcQXzIw6KRacx1721da2oN2SM/pubhtml) and the data for caught fish can be editted by anybody but the site that I used for mine is [ac-catch](https://ac-catch.com/) and [nook.lol](https://nook.lol/). It doesn't matter where the input data is from but it just needs to include the proper fish names (`blue_marlin` vs `blue marlin`)[^1] and one fish per row. The file can also contain other random info but if it isn't a fish that is properly named to match the fish in the datasheet, it will be ignored.

[^1]: I do have it automatically replace underscores with spaces, since ac-catch uses underscores.

## Potential Next Steps:
- Highlight caught fish in a different color on the spawning calendar.
- Allow filtering to display only caught fish in the heatmap.
- Provide additional details like selling price, location, etc.

## Todo list:
- For each month, calculate the number of caught fish vs the number of available fish in that month and then use that to suggest months to fish during.
   - Considerations: Fish spawn in different sizes, bait allows for "rerolling" of fish sizes, it might be better to compare fish based on size first e.g. if there are 10 new fish in a month but they are all small fish and the next month there are also 10 new fish but 5 small (same small fish from last month) and 5 large, it would be better to fish in the next month, assuming that the other 5 small fish spawn at another time...? I need to think about this more...
