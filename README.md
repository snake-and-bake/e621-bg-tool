# E621 Random Background Download

This script uses the `e621-stable` pip library to grab posts from https://e621.net and downloads a random image based on your constraints. It's intended to get desktop wallpaper-worthy aspect ratios.

There's a tutorial and some helpful hints in the CLI. 

NOTE: This requires python3.12 (maybe 3.11, i forget when fstring changes were introduced) - this is why the docker path is suggested.

# Installation & Usage

1. Clone this repo with `git clone https://github.com/snake-and-bake/e621-bg-tool.git`
2. cd into the repo with `cd e621-bg-tool`

## Docker Option (Recommended)

2. run `docker build -t e621bg .` 
3. run `./launch_in_docker.sh`

## Local Environment Option

2. Create a python 3 virtual environment with `python3 -m venv .venv`
3. Enter the venv with `source .venv/bin/activate`
4. Install the required dependencies with `python3 -m pip install requirements.txt`
5. Navigate to the directory you want your images to be stored in with `cd /path/to/image/folder`
6. Run the script with `python3 /path/to/e21bgrandomizer/e621bg.py`
