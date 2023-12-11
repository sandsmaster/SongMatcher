from pyglet.media import Player, load
import asyncio.futures
import time

def pick_option(picks_list):
    show_menu()
    # with asyncio.futures.ThreadPoolExecutor() as executor:
    #     pass
    while True:
        choice = input("Pick an option: ")
        if choice in picks_list:
            return choice
        else:
            print(f"You need to pick from the list\nThe List: {', '.join(picks_list)}")


def show_menu():
    print("a) Play game")
    print("b) Add a song")
    print("c) Highscores")


def game():
    pass


def add_song():
    pass


def highscore():
    pass


def main():
    options = ["a", "b", "c"]
    choice = pick_option(options)
    if choice == options[0]:
        game()
    elif choice == options[1]:
        add_song()
    elif choice == options[2]:
        highscore()



if __name__ == "__main__":
    main()