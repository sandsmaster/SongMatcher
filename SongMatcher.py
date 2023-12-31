import time
from pyglet.media import Player, load
from random import randint, shuffle, choice
from os import listdir, path
from shutil import copyfile
import ctypes, sys
import tkinter as tk
from tkinter import filedialog
from csv import DictReader

from tabulate import tabulate

CURR_PATH = path.abspath(r'.')

def pick_option(picks_list, menu_arg = None):
    if menu_arg:
        show_menu()
    while True:
        choice = input("Pick an option: ").strip()
        if choice in picks_list:
            return choice
        else:
            print(f"You need to pick from the list\nThe List: {', '.join(picks_list)}")


def show_menu(choice = "main", *args):
    if choice == "main":
        print("a) Play game")
        print("b) Add a song")
        print("c) Highscores")
        print("q) Exit")
    elif choice == "songs":
        print("\nWhich is the song playing?:")
        # args must have song names inside of it
        for i, song in enumerate(args):
            print(f"{i + 1}) {song}")   # print the song name with option letter next to it


def play_song_from_time(file_path, media_player, play_from = 0, random_time = True):
    src = load(file_path)
    media_player.queue(src)
    if media_player.playing:
        if media_player.source.duration != src.duration:
            print("☻ Went to next source!")
            media_player.delete()
            media_player.next_source()
            media_player.pause()

    if random_time:
        play_from = randint(0, int(media_player.source.duration)-20)
    media_player.source.seek(play_from)
    media_player.play()


def play_round():
    ANSWER_COUNT = 4
    options = listdir("samples/.")  # get all songs with "samples/" infront of them
    shuffle(options)
    options = options[0:ANSWER_COUNT]
    correct_guess = choice(options) # pick random song to play
    
    media_player = Player()
    play_song_from_time(f'samples/{correct_guess}', media_player, random_time=True)
    print("Playing random song...")

    show_menu("songs", *options)
    # print(f"Hint: Pick {correct_guess} to guess right")   # cheat code :d
    guess = int(pick_option([str(num + 1) for num in range(ANSWER_COUNT)])) - 1 # conver range() to str and decrease 1, 
                                                                                # because user picks 1-based options

    if correct_guess == options[guess]:
        print("\nGood Job! You guessed right.\n")
        return True
    print("\nNice try, but you didn't guess.\n")
    return False
    

def play_again(score):
    print("\nThe game finished!")
    print(f"Your final score is {score}.")
    if input("Play again? (y)es/(n)o: ").strip().lower() in ["y", "yes"]:
        return True
    return False


def save_highscore(score, score_file_name, score_header):
    with open(score_file_name, 'a') as file:
        name = input("What's your name?: ")
        file.write(f"\n{name},{str(score)}")
    
    print("Highscore successfully saved")


def game(score_file_name, score_header):
    ROUND_COUNT = 5
    new_game = True
    
    while new_game:
        score = 0
        for _ in range(ROUND_COUNT):
            if (play_round()):
                score += 1

        if not path.exists(path.join(CURR_PATH,score_file_name)):
            print("File missing. Creating new one...")
            create_highscore_csv(score_file_name, score_header)
        save_highscore(score, score_file_name, score_header)
        
        new_game = play_again(score)


def add_song():
    src = filedialog.askopenfilename()
    dst = r"C:\Users\botcho\Desktop\Projects\Py Stuff\SongMatcher\samples" + "\\" + src.split("/")[-1]    # Take the name of the song
    print(dst)
    time.sleep(1)
    if path.isfile(src):
        copyfile(src, dst)
        print("Song added successfully!")
    else:
        print("No song added.")


def load_highscore(score_file_name):
    print("Reading Highscores\n")
    scores = []

    with open(score_file_name, "r") as score_file:  # read highscores file
        score_csv = DictReader(score_file)
        for row in score_csv:
            scores.append(row.values())
    return scores


def create_highscore_csv(score_file_name, score_header):
    with open(score_file_name, "w") as file:
        file.write(",".join(score_header))


def highscore(score_file_name, score_header):
    if path.isfile(score_file_name):                            # if file exists
        scores = load_highscore(score_file_name)  # get highscore data
        print(tabulate(scores, score_header))                   # pretty print

    else:   # if file doesn't exist
        print("Doesn't exist. \nCreating highscore file...")
        create_highscore_csv(score_file_name, score_header)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def main():
    #get_admin()
    options = ["a", "b", "c", "q"]
    score_file_name = "highscore.csv"
    score_header = ["Player", "Score"]
    root = tk.Tk()  # used to open file dialog
    root.withdraw()

    while True:
        choice = pick_option(options, "main")
        if choice == options[0]:
            game(score_file_name, score_header)
        elif choice == options[1]:
            add_song()
        elif choice == options[2]:
            highscore(score_file_name, score_header)
        elif choice == options[3]:
            break


if __name__ == "__main__":
    main()