![Repo Banner](https://github.com/Jukelyn/acnh-fish-chart/blob/main/static/images/repo_banner.png?raw=true&v=2)

<div align="center">
   
   ![Website](https://img.shields.io/website?url=https%3A%2F%2Facnh-fish.jukelyn.com&up_message=Up&down_message=Down&label=Site%20Status&cacheSeconds=10)
   ![Pylint Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/pylint.yaml/badge.svg)
   ![Docker Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/restart_docker.yaml/badge.svg)
   ![SFTP Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/sftp.yaml/badge.svg)
   ![Super Linter Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/super-linter.yaml/badge.svg)

### Built using

![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=plastic&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=plastic&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=plastic&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=plastic&logo=javascript&logoColor=%23F7DF1E)

### Deployed on

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=plastic&logo=ubuntu&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=plastic&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=nginx&logoColor=white)

</div>

# ACNH Fishing Tracker/Guide

A simple site for tracking fish and finding the best months to fish to complete the Critterpedia!

## Current Features

1. **Reads fish spawning data** from `data/fish_datasheet.csv`, extracting all fish names and their spawning months.
2. **Creates two main DataFrames:**
   - `NH_df` → Contains fish names and their **Northern Hemisphere** spawning months.
   - `SH_df` → Contains fish names and their **Southern Hemisphere** spawning months.
3. **Generates spawning calendar** for the chosen hemispheres:
   - Rows: Fish names
   - Columns: Months (January–December)
   - Green cells: Indicate spawning months
4. **Ability to input** fish that have been caught:
   - Inputs fish data via a form
   - Checks for the valid fishes and removes them from the *uncaught list*

## Information

The fish spawning data is from [this spreadsheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vTGrIfAI5ybCvaiIux5kEbermRFZe6aooAs7I1iVrJF27DrXSOJQxxEcQXzIw6KRacx1721da2oN2SM/pubhtml)
and the data for caught fish can be editted by anybody but the site that I used for mine is
[ac-catch](https://ac-catch.com/) and [nook.lol](https://nook.lol/).
It doesn't matter where the input data is from but it just needs to include the proper
fish names (`blue_marlin` vs `blue marlin`) and one fish per row. The file can also
contain other random info but if it isn't a fish that is properly named to match the fish in the datasheet, it will be filtered and a fuzzy matching algorithm will be used to suggest what fishs the input may be for.

See fuzzy matching below:
<div align="center">
   
![Method img](https://github.com/Jukelyn/acnh-fish-chart/blob/main/static/images/get_closest_match_image_transparent.png)

</div>

## Potential Next Steps

- Highlight caught fish in a different color on the spawning calendar. (Or simply remoze them from the image instead)
- Allow filtering to display only caught fish in the heatmap. (Depends on what I choose to do above)
- Provide additional details like selling price, location, etc. (Instead opting for making cards with the fish info instead)

### **Notes for Development:**

#### Step 1: Gather Fish Data

1. **Make a List of All Fish Caught**

   - Check the in-game Critterpedia or use nook.lol or another site.
   - Input the data.

2. **Get a Full Fish Availability Chart**
   - Make a monthly fish availability table for each hemisphere.
   - Ensure it lists which fish spawn each month.

---

#### Step 2: Identify the Best Next Fishing Month

1. **Compare Caught Fish Against Each Month**

   - Count how many **new (uncaught)** fish appear in each month.
   - Count how many **previously caught** fish also appear.

2. **Choose the Month with the Highest New-to-Old Ratio**
   - Prioritize months where **many new fish spawn** and **fewer caught fish overlap**.
   - Avoid months where most fish are ones you've already caught.

---

#### Step 3: Plan a Sequence of Months

1. After selecting the best next month, repeat **Step 2** to find the next best month.
2. Continue until you have caught all fish with minimal duplication.

---

Example Scenario

- You’ve caught **50 out of 80 fish** in the Northern Hemisphere.
- Checking a **monthly fish chart**, you find:
  - **June:** 15 new fish, but 35 duplicates.
  - **October:** 12 new fish, but only 20 duplicates.
- **October is a better choice** because it minimizes duplicate catches.

---

- Sort by the best ratio of new vs. previously caught fish.
