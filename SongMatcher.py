from pyglet.media import Player, load
import asyncio.futures
from random import randint
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


def play_song_from_time(media_player, song_path, play_from = 0, random_time = True):
    src = load(song_path)
    media_player.queue(src)
    if random_time:
        play_from = randint(0, int(media_player.source.duration))
    media_player.source.seek(play_from)
    media_player.play()


def play_round(media_player):
    play_song_from_time(media_player, r'samples/ei_tuka_ei_tei.mp3', random_time=True)
    print(f"Total Song Duration: {media_player.source.duration}")
    print("Playing random part...")
    time.sleep(20)
    

def game():
    print('''The rules are simple. You have to guess the song. 
          Press Enter when you are ready to answear.
          You have 1-30 seconds to guess the song''')

    player = Player()
    play_round(player)


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