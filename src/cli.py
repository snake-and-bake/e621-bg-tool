"""
DOCSTRING GO HERE
"""

import argparse
from pathlib import Path
from itertools import combinations_with_replacement

# TODO: move these to a config file
genders = [
    "male",
    "female",
    "gynomorph",
    "andromorph",
]
combos = combinations_with_replacement(genders, 2)
choices = genders + [f"{x}/{y}" for x, y in combos]

print(choices)


def parse_args():
    parser = argparse.ArgumentParser(description="")
    # output_text = parser.add_mutually_exclusive_group()
    # output_text.add_argument("-v", "--verbosity", action="count", default=1)
    # output_text.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument(
        "-c",
        "--count",
        action="store",
        type=int,
        default=1,
        help="The number of images to save.",
    )
    parser.add_argument(
        "-b",
        "--block",
        action="store",
        type=str,
        help="Keywords to exclude from search results.",
        nargs="*",
    )
    parser.add_argument(
        "-k",
        "--keywords",
        action="store",
        type=str,
        help="Keywords to include in search results.",
        nargs="*",
    )
    parser.add_argument(
        "-s",
        "--score",
        action="store",
        type=int,
        help="The lowest acceptable image score.",
    )
    parser.add_argument(
        "-g",
        "--genders",
        choices=choices,
        action="store",
        type=str,
        help="The gender or gender pairings you want to include in your search.",
    )
    parser.add_argument(
        "-p",
        "--path",
        action="store",
        default=".",
        type=Path,
        help="The absolute or relative filepath where you wish to save your photos.",
    )
    # parser.add_argument(
    #     "-i",
    #     "--interactive",
    #     action="store_true",
    #     help="Enable an interactive session.",
    # )
    parser.add_argument(
        "-t",
        "--time",
        action="store",
        type=str,
        help="The relative or absolute date for your search results.",
    )
    # parser.add_argument(
    #     "--config",
    #     action="store",
    #     type=Path,
    #     help="The absolute or relative filepath to your configuration file.",
    # )
    image_dimensions = parser.add_mutually_exclusive_group()
    image_dimensions.add_argument(
        "-r",
        "--ratio",
        action="store",
        type=float,
        default=1.0,
        help="The aspect ratio you wish to collect images in",
    )
    image_dimensions.add_argument(
        "-d",
        "--display",
        action="store",
        type=int,
        help="The X and Y pixel values to be used as an alternative to aspect ratios.",
        nargs=2,
    )
    return parser.parse_args()
