"""
what the fuck do I want, from the simplest to the most complex?

- run the script, grab a picture from e621
- run the script with a COUNT arg, get COUNT pictures from e621
- run the script with a KEYWORDS arg, get only pictures matching the tags
- run the script with a SCORE arg, get only pictures with a score of SCORE or higher
- run the script with a BLOCK arg, get only pitcutres that DO NOT match the tags
- run the script with a GENDERS arg, get only pictures that contain the specified gender or gender pairing
- run the script with a PATH arg, save pictures to the specified path instead of .
- run the script with a RATIO arg, get only pictures that match (or are within 1% (????) of) the specifed ratio
- run the script with a DISPLAY arg, get only pictures that match the ratio-ish of the WidthxHeight added
- run the script with the INTERACTIVE flag, and go through a script that runs through all the stuff with you



i feel like there's other things here that i wanna add, like different ways of picking and examples like POTD or automatic detection of resolution....


but let me just start rewriting everything in the original script so i don't have to worry about all that now.

"""

import requests
import tkinter
from e621.api import E621
from pathlib import Path
from src import cli

# TODO: export these funcs to more objects


def grab_posts(query, limit):
    api = E621()
    return api.posts.search(query, limit=limit, ignore_pagination=True)


def save_photo(dir, post, ratio):
    destination = Path(dir) / ratio
    if not destination.exists():
        destination.mkdir()
    destination = destination / f"{post.id}.{post.file.ext}"
    if not destination.exists():
        try:
            with open(destination, "wb") as file:
                file.write(requests.get(post.file.url).content)
            return True
        except:
            raise Exception("Saving photo failed!!!")


def create_query(args):
    query = ""
    if args.keywords:
        query += " ".join(args.keywords)
    if args.block:
        query += " -".join(args.block)
    if args.genders:
        query += " ".join(args.genders)
    if args.score:
        query += f" score:>={args.score}"
    if args.time:
        query += f" date:{args.time}"
    # NOTE: I feel like this is bad... Should I be modifying args.ratio directly?
    if not args.ratio and not args.display:
        display = tkinter.Tk()
        args.ratio = display.winfo_screenwidth() / display.winfo_screenheight()
    if args.display:
        args.ratio = args.display[0] / args.display[1]
    if args.ratio:
        query += f" ratio:{args.ratio}"
    return query


def main():

    print("starting...")
    args = cli.parse_args()

    # TODO: error handling
    count = args.count
    query = create_query(args)
    print(f"Searching for {query}")

    posts = grab_posts(query, count)

    if len(posts) < count:
        print("Less posts than requested, exiting...")
        exit(1)

    for post in posts:
        save_photo(args.path, post, args.ratio)

    print("done!")


if __name__ == "__main__":
    main()
