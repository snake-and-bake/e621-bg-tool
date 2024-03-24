# E621 Random Background Download

This script uses the `e621-stable` pip library to grab posts from https://e621.net and downloads a random image based on your constraints. It's intended to get desktop wallpaper-worthy aspect ratios.

There's a tutorial and some helpful hints in the CLI. I'll put this in a docker container ASAP!

# Installation & Usage

1. Clone this repo with `git clone https://github.com/snake-and-bake/e621bgrandomizer.git`
2. Create a python 3 virtual environment with `python3 -m venv .venv`
3. Enter the venv with `source .venv/bin/activate`
4. Install the required dependencies with `python3 -m pip install requirements.txt`
5. Navigate to the directory you want your images to be stored in with `cd /path/to/image/folder`
6. Run the script with `python3 /path/to/e21bgrandomizer/e621bg.py`
