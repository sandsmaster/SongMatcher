import time
import colorama
from pyglet.media import Player, load
from random import randint, shuffle, choice
from os import listdir, path, mkdir
from shutil import copyfile
import ctypes, sys
import tkinter as tk
from tkinter import filedialog
from csv import DictReader

from tabulate import tabulate


def sort_scores(scores, sort_col_num):
    if type(scores) != list:
        raise TypeError("Scores is not a list!")
    if len(scores) <= 0:
        raise IndexError("No items inside of scores!")
    if type(scores[0]) != list:
        raise TypeError("Scores doesn't contain lists of scores!")
    
    return sorted(scores, reverse=True, key=lambda score: score[sort_col_num])  # return sorted scores


def del_extension(song_name: str):
    if type(song_name) != str:
        raise TypeError("You must pass a string")
    if song_name.find(".") == -1 or song_name[-1] == ".":
        raise IndexError("Couldn't find . (dot). This is not a valid file name")
    return song_name[:song_name.rfind(".")] # cut file extension from name (.mp3, .wav,...)


def is_correct_guess(correct_guess, other_guess):
    if correct_guess == other_guess:
        print(colorama.Fore.GREEN + "\nGood Job! You guessed right.\n")
        print(colorama.Fore.RESET)
        return True
    print(colorama.Fore.RED + "\nNice try, but you didn't guess.\n")
    print(colorama.Fore.RESET)
    return False


def color_print(color, msg):
    print(color + msg)
    print(colorama.Fore.RESET)


def pick_option(picks_list):
    while True:
        choice = input("Pick an option: ").strip()
        if choice in picks_list:
            return choice
        else:
            color_print(colorama.Fore.RED, f"You need to pick from the list\nThe List: {', '.join(picks_list)}")


def pick_number(message, min=None, max=None):
    number = 0
    while True:
        try:
            number = int(input(message))
        except ValueError:
            clear_scr()
            color_print(colorama.Fore.RED, "You need to pick a NUMBER. This isn't one")
            continue

        if min is not None:
            if number < min:
                clear_scr()
                color_print(colorama.Fore.RED, f"Number must be bigger than {min - 1}")
                continue
        if max is not None:
            if number > max:
                clear_scr()
                color_print(colorama.Fore.RED, f"Number must be smaller than {max + 1}")
                continue
    
        return number
    

def clear_scr():
    print("\033[H\033[J", end="")


def wait_user():
    input("Press enter to continue...")


class SongMatcherGame():
    CURR_PATH = path.abspath(r'.')    
    score_file_name = "highscore.csv"
    score_header = ["Player", "Score"]
    root = tk.Tk()  # used to open file dialog

    def __init__(self, round_count, answer_count) -> None:
        self.round_count = round_count
        self.answer_count = answer_count


    def show_menu(self, choice = "main", *args, clear_screen=False):
        if clear_screen:
            clear_scr()
        if choice == "main":
            print(colorama.Fore.BLUE + "a) Play game")
            print(colorama.Fore.BLUE + "b) Add a song")
            print(colorama.Fore.BLUE + "c) Highscores")
            print(colorama.Fore.BLUE + "d) Settings")
            print(colorama.Fore.RED + "q) Exit")
            print(colorama.Fore.RESET)
        elif choice == "songs":
            print("\nWhich is the song playing?:")
            # args must have song names inside of it
            for i, song in enumerate(args):
                print(colorama.Fore.BLUE + f"{i + 1}) {song}", end="")   # print the song name with option letter next to it
                print(colorama.Fore.RESET)
        elif choice == "settings":
            print(f"1) Round count [{self.round_count}]")
            print(f"2) Answer count [{self.answer_count}]")
            print(colorama.Fore.RED + f"q) Quit")
            print(colorama.Fore.RESET)
        else:
            raise NameError("choice must be either 'menu' or 'songs'")


    def play_song_from_time_check_par_type(self, file_path, media_player, play_from, random_time):
        if type(file_path) != str:
            raise TypeError("File path for song isn't string")
        if type(media_player) != Player:
            raise TypeError("Media player for song isn't of type Player from pyglet")
        if type(play_from) != int:
            raise TypeError("Song start time (play_from) for song isn't integer")
        if type(random_time) != bool:
            raise TypeError("random_time for song isn't boolean")


    def play_song_from_time(self, file_path, media_player, play_from = 0, random_time = True):
        self.play_song_from_time_check_par_type(file_path, media_player, play_from, random_time)
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


    def get_songs(self, sample_dir="samples/."):
        try:
            options = listdir(sample_dir)      # get all songs from samples folder
        except FileNotFoundError:
            print("Samples folder doesn't exist. Creating one...")
            sample_dir = path.join(self.CURR_PATH,"samples/.")
            mkdir(sample_dir)
            return None
        if not options:                     # No songs in the list
            print("There are no songs in the samples folder. Please add a few to play")
            wait_user()        
            return None
        if len(options) < self.answer_count:    # Less songs then needed wanted
            print(f"There are not enough songs in samples folder. Please add more songs or change answer count from settings")
            wait_user()
            return None
        shuffle(options)                    # shuffle
        return options[0:self.answer_count] # return n songs


    def play_round(self):
        options = self.get_songs()
        if options == None:
            return None
        correct_guess = choice(options) # pick random song to play
        
        media_player = Player()
        self.play_song_from_time(f'samples/{correct_guess}', media_player, random_time=True)
        print("Playing random song...")

        options_clean = list(map(del_extension, options)) # remove extensions before showing menu

        self.show_menu("songs", *options_clean, clear_screen=True)
        # print(f"Hint: Pick {correct_guess} to guess right")   # cheat code :d
        guess = int(pick_option([str(num + 1) for num in range(self.answer_count)])) - 1 # conver range() to str and decrease 1, 
                                                                                    # because user picks 1-based options
        is_correct = is_correct_guess(correct_guess, options[guess])
        wait_user()    # wait for user outside, because it's easier to test is_correct_guess
        return is_correct
        

    def play_again(self, score):
        if type(score) != int:
            raise TypeError("Score must be an integer") # Error Handling

        print("\nThe game finished!")
        print(f"Your final score is {score}.")
        if input("Play again? (y)es/(n)o: ").strip().lower() in ["y", "yes"]:
            return True
        return False


    def save_highscore(self, score):
        if type(score) not in [int, str]:
            raise TypeError("Score must be an integer or string")   # Error Handling
        
        with open(self.score_file_name, 'a') as file:
            name = input("What's your name? (Leave blank to skip): ").strip()
            if not name:
                return False
            file.write(f"\n\"{name}\",{str(score)}")
        
        print("Highscore successfully saved")


    def game(self):
        new_game = True

        while new_game:
            score = 0
            for _ in range(self.round_count):
                round_result = self.play_round()
                if (round_result) == True:
                    score += 1
                elif (round_result) == None:
                    return False

            if not path.exists(path.join(self.CURR_PATH, self.score_file_name)):
                print("File missing. Creating new one...")
                self.create_highscore_csv()
            self.save_highscore(score)
            
            new_game = self.play_again(score)


    def add_song(self):
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        src = filedialog.askopenfilename()
        dst = self.CURR_PATH + r"\samples" + "\\" + src.split("/")[-1]    # Take the name of the song
        print(dst)
        time.sleep(1)
        if path.isfile(src):
            copyfile(src, dst)
            print("Song added successfully!")
        else:
            print("No song added.")
        wait_user()


    def load_highscore(self):
        scores = []

        with open(self.score_file_name, "r") as score_file:  # read highscores file
            score_csv = DictReader(score_file)
            for row in score_csv:
                scores.append(list(row.values()))
        return sort_scores(scores, 1)


    def create_highscore_csv(self):
        with open(self.score_file_name, "w") as file:
            file.write(",".join(self.score_header))


    def highscore(self):
        clear_scr()
        if path.isfile(self.score_file_name):                            # if file exists
            scores = self.load_highscore()  # get highscore data
            print(tabulate(scores, self.score_header))                   # pretty print

        else:   # if file doesn't exist
            print("Doesn't exist. \nCreating highscore file...")
            self.create_highscore_csv()
        print()             # Separate highscore with next output
        wait_user()


    def settings(self):
        setting_options = ["1", "2", "q"]
        while True:
            clear_scr()
            self.show_menu("settings")
            pick = pick_option(setting_options)

            if pick == "1":
                self.round_count = pick_number("Change round count to: ", min=1)
            elif pick == "2":
                self.answer_count = pick_number("Change answer count to: ", min=2)
            elif pick == "q":
                break


    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


    def get_admin(self):
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


    def main(self):
        #get_admin()
        options = ["a", "b", "c", "d", "q"]
        self.root.withdraw()

        while True:
            clear_scr()
            self.show_menu()
            choice = pick_option(options)
            if choice == options[0]:    # a
                self.game()
            elif choice == options[1]:  # b
                self.add_song()
            elif choice == options[2]:  # c
                self.highscore()
            elif choice == options[3]:  # c:
                self.settings()
            elif choice == options[4]:  # q
                break
            
        clear_scr()


def main():
    SongMatcherGame(round_count=3, answer_count=4).main()


if __name__ == "__main__":
    main()