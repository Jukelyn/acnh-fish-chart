![Repo Banner](https://github.com/Jukelyn/acnh-fish-chart/blob/main/static/images/repo_banner.png?raw=true&v=2)

<div align="center">
   
   ![GitHub License](https://img.shields.io/github/license/Jukelyn/acnh-fish-chart?label=License&color=springgreen)
   ![Website](https://img.shields.io/website?url=https%3A%2F%2Facnh-fish.jukelyn.com&up_message=Up&up_color=springgreen&down_color=crimson&down_message=Down&label=Site%20Status&cacheSeconds=10)
   ![Pylint Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/pylint.yaml/badge.svg?color=springgreen)
   ![Docker Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/restart_docker.yaml/badge.svg?color=springgreen)
   ![SFTP Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/sftp.yaml/badge.svg?color=springgreen)
   ![Super Linter Workflow Status Badge](https://github.com/Jukelyn/acnh-fish-chart/actions/workflows/super-linter.yaml/badge.svg?color=springgreen)

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
   - Checks for the valid fishes and removes them from the _uncaught list_

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

## Local Development

The site is written using Flask and mostly HTML and JS. In order to host a local version of the site, these are the reccomended instructions:

1. Have Python and pip installed
2. Clone the repo

   ```bash
   git clone https://github.com/Jukelyn/acnh-fish-chart.git

   ```
3. Enter the repo and create a virtual enviornment (venv)

   ```
   cd acnh-fish-chart && python3 -m venv venv

   ```
4. Activate the venv

   POSIX bash/zsh:
   ```bash
   source venv/bin/activate
   ```
   Windows:
   ```cmd
   C:\> <venv>\Scripts\activate.bat
   PS C:\> <venv>\Scripts\Activate.ps1 // Don't do this though, why are you using PowerShell?
   ```
5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
6. Host a local server
   ```bash
   python run.py
   ```
The site should now be available on `127.0.0.1:5000` (or whatever other IP/port you set in `src/__init__.py`)

<hr />

## Docker Deployment

1. Follow the previous steps 1 to 5.
2. [Build](https://docs.docker.com/build/concepts/dockerfile/#building) the docker image from the provided Dockerfile. (You can also just do step 3, it will build it for you)
3. Change the `docker-compose.yaml` file to use the networks that you have defined, or remove the network fields if you want to have it create it's own automatically.
4. Add port to forward, if needed. If you are using a reverse proxy on the same server, you don't need to do this, just forward your (sub)domain to the container on the port directly. (Default: 5000)
- If you change the port, make sure to change it in `src/__init__.py` as well as `Dockerfile`.
6. Run `docker compose up -d`
7. Navigate to the IP:port or (sub)domain that you assigned in your reverse proxy.

<hr />
