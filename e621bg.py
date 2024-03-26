"""
pylint got mad at me so i had to put the doctring here
"""

from datetime import date
from pathlib import Path
from random import randrange
from time import sleep

import requests
from e621 import E621

api = E621()

ESSENTIALS = "rating:explicit -young -animated -watersports -scat -rape -hyper -vore -blood -crying -zaush -bestiality -portal"
ratios = ["0.46", "1", "1.6", "1.77", "2.38"]
genders = ["male", "female", "andromorph", "gynomorph"]
RETURN_LIMIT = 1024
desktop_wallpaper_directories = Path(".")
INITIAL_STANDARDS = 500


def nap():
    sleep(0.5)


def rest():
    sleep(1)


def run_tutorial(selection):

    tutorial = [
        "Welcome to the Tutorial!",
        "This script will download random images from e621 for whatever purpose you need.",
        "From there, you decide how many images you want to download, and how random you want the images to be.",
        "In the default configuration, any gender or gender pairing is allowed and dimensions are restricted to wallpaper-friendly ratios.",
        "All images will be saved in the same folder you run this script from - not necssarily the same folder the script is in!",
        "New folders will be created if they do not already exist.",
    ]

    hints = [
        'There is a pre-filled list of search filters near the top of this script called "ESSENTIALS". Edit it to your personal tastes!',
        "To stay polite, the search is limited to 1024 entries per query. Adjust this up or down if needed.",
        "If you select both Solo and Multiple Characters and have a particular gender you want to avoid solo, add it second so it only shows up in pairings.",
        "If you don't know your monitor's fractional ratio, replace the colon with a divison symbol, or divide monitor width by height.",
        "e.g. 16:9 == 16 / 9 == 1.77...; 1920 / 1080 == 1.77...",
    ]

    if selection == "F":
        choice = ["M", "T"]
    else:
        choice = selection

    if "M" in choice:
        for line in tutorial:
            print(line)
            nap()

    if "T" in choice:
        for line in hints:
            print(line)
            nap()

    input("Press enter to return to the main application.")
    return


def choose_random(options):
    return options[randrange(len(options))]


def single_or_multi():
    return randrange(2)


def choose_genders():

    options = {"1": "Solo", "2": "Multiple Characters"}
    print(
        "Choose Solo or Multiple Characters:\n1) Solo\n2) Multiple\nNone/Any) Randomly Choose"
    )
    count_choice = input("> ")
    count = 0

    if count_choice in options:
        print(f"{options[count_choice]} selected!")
        count = int(count_choice)
    else:
        print("Random selected!")

    print("Please select a gender:")
    gender_list = f"{'\n'.join([f'{index}) {value}' for index, value in enumerate(genders)])}\nNone/Any) Randomly Choose\n> "
    first_gender = input(gender_list)
    gender_range = range(len(genders))

    if first_gender != "":
        if int(first_gender) in gender_range:
            first_gender = int(first_gender)
        else:
            first_gender = choose_random(gender_range)
    else:
        first_gender = choose_random(gender_range)

    if count == 1:
        return f"{genders[first_gender]} solo"
    print("Please select another gender:")

    second_gender = input(gender_list)
    if second_gender != "":
        if int(second_gender) in gender_range:
            second_gender = int(second_gender)
        else:
            second_gender = choose_random(gender_range)
    else:
        second_gender = choose_random(gender_range)

    return f"{genders[first_gender]}/{genders[second_gender]}"


def choose_ratios():
    return choose_random(ratios)


def calclulate_bounds(ratio):
    value = float(ratio)
    offset = 1 / 100
    return str(value - (value * offset)), str(value + (value * offset))


def photo_already_exists(image_id):
    try:
        photos = list(desktop_wallpaper_directories.glob("**/*.*"))
        for photo in photos:
            if str(image_id) in photo.name:
                return True
        return False
    except:
        raise Exception("Photo Check failed!")


def save_photo(post, ratio):
    destination = desktop_wallpaper_directories / ratio
    if not destination.exists():
        destination.mkdir()
    destination = destination / f"{post.id}.{post.file.ext}"
    try:
        with open(destination, "wb") as file:
            file.write(requests.get(post.file.url).content)
        return True
    except:
        raise Exception("Saving photo failed!!!")


def main():
    print("Welcome to the E621 Desktop Background Manager!")
    want_tutorial = input(
        "Do you want the full tutorial, or just the tips? (;3)\n(F)ull tutorial\n(T)ips\n(None/Any) Neither\n> "
    )
    if len(want_tutorial) == 0:
        want_tutorial = "N"
    if want_tutorial[0].upper() in ["F", "T"]:
        run_tutorial(want_tutorial[0].upper())
    print("Starting...")
    repeat = True
    while repeat:
        print("How many images do you want to pull?")
        print(f"Please enter a number between 1 and {RETURN_LIMIT}.")
        count = input(f"Default: 10\n> ")
        if count == "" or int(count) < 1:
            count = 10
        elif int(count) > RETURN_LIMIT:
            count = RETURN_LIMIT
        else:
            count = int(count)
        ratio = ""
        gender_pairing = ""
        standards = INITIAL_STANDARDS
        gender_pairing = choose_genders()
        ratio = input(
            f'Enter a ratio between 0.02 and 26.55.\nTypical Ratios:{" ".join(ratios)}\nEnter nothing for a random typical ratio.\n> '
        )
        if len(ratio) == 0:
            print("Choosing Ratio...")
            ratio = choose_ratios()
        print(f"{ratio} chosen!\nGenerating query...")
        lower, upper = calclulate_bounds(ratio)
        query = (
            f"{ESSENTIALS} score:>{standards} ratio:{lower}..{upper} {gender_pairing}"
        )
        print(f"Query: {query}\nSearching for posts...")
        try:
            grab_posts = lambda x: x.posts.search(
                query, limit=RETURN_LIMIT, ignore_pagination=True
            )
            posts = grab_posts(api)
            print(f"Pulled {len(posts)} images!")
            if len(posts) == 0:
                while len(posts) == 0:
                    if standards <= 0:
                        raise Exception("No posts found!!!")
                    print("No posts found! Trying again with lower standards...")
                    standards -= 10
                    query = f"{ESSENTIALS} score:>{standards} ratio:{lower}..{upper} {gender_pairing}"
                    posts = grab_posts(api)
            allowable_drop_in_standards = None

            while len(posts) < count:
                print("Not enough posts found!")
                if allowable_drop_in_standards == None:
                    allowable_drop_in_standards = input(
                        f"Current standards: {standards}\nHow much can the standards allowable_drop_in_standards before you give up? (Default: 0.5)\n> "
                    )
                if allowable_drop_in_standards == "":
                    allowable_drop_in_standards = 0.5
                else:
                    allowable_drop_in_standards = float(allowable_drop_in_standards)
                standards -= 10
                if standards <= 0:
                    raise Exception("No good posts found!!!")

                query = f"{ESSENTIALS} score:>{standards} ratio:{lower}..{upper} {gender_pairing}"
                print(f"Trying again with a score of {standards}...")
                posts = grab_posts(api)
                print(f"Pulled {len(posts)} images!")
                if (
                    len(posts) > 0
                    and standards <= INITIAL_STANDARDS * allowable_drop_in_standards
                ):
                    print(
                        "There are posts, but not enough posts to meet the requested amount. Adjusting count..."
                    )
                    count = len(posts)
                    break
        except:
            raise Exception("e621 Search failed!!!")

        saved_posts = 0
        while saved_posts < count:
            print("Selecting random post...")
            post = choose_random(posts)
            already_exists = []
            while photo_already_exists(post.id):
                print("Post already exists! Selecting another...")
                already_exists.append(post.id)
                if len(already_exists) == len(posts):
                    raise Exception("All images already saved!")
                post = choose_random(posts)
            print(f"Post from {post.tags.artist} selected!\nSaving photo...")
            if save_photo(post, ratio):
                print("Saved!")
                saved_posts += 1
                print(f"{saved_posts} of {count} saved!")
        print("All done! Enjoy :3")
        if input("Do you want to run this again? (Y/N)\n> ").upper() != "Y":
            repeat = False


if __name__ == "__main__":
    main()
