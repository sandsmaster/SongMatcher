from pyglet.media import Player, load
import asyncio.futures
from random import randint, shuffle
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


def show_menu(choice = "main", *args):
    if choice == "main":
        print("a) Play game")
        print("b) Add a song")
        print("c) Highscores")
    elif choice == "songs":
        print("\nWhich is the song playing?:")
        # args must have song names inside of it
        for i, song in enumerate(args):
            print(f"{i + 1}) {song}")   # print the song name with option letter next to it


def play_song_from_time(media_player, song_path, play_from = 0, random_time = True):
    src = load(song_path)
    media_player.queue(src)
    if random_time:
        play_from = randint(0, int(media_player.source.duration)-20)
    media_player.source.seek(play_from)
    media_player.play()


def play_round(media_player):
    correct_guess = r'samples/ei_tuka_ei_tei.mp3'

    play_song_from_time(media_player, r'samples/ei_tuka_ei_tei.mp3', random_time=True)
    print(f"Total Song Duration: {media_player.source.duration}")
    print("Playing random part...")

    options = [r'samples/ei_tuka_ei_tei.mp3', r'samples/high.mp3', r'samples/pianata_toqga.mp3']
    shuffle(options)
    show_menu("songs", *options)
    
    guess = int(pick_option([str(x + 1) for x in range(3)])) - 1

    if correct_guess == options[guess]:
        return True
    return False
    

def game():
    print('''The rules are simple. You have to guess the song. 
          Press Enter when you are ready to answear.
          You have 1-30 seconds to guess the song''')

    player = Player()
    print(play_round(player))


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