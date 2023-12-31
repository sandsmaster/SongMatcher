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


class SongMatcherGame():
    CURR_PATH = path.abspath(r'.')    
    score_file_name = "highscore.csv"
    score_header = ["Player", "Score"]

    def __init__(self, round_count, answer_count) -> None:
        self.round_count = round_count
        self.answer_count = answer_count


    def pick_option(self, picks_list, menu_arg = None):
        if menu_arg:
            self.show_menu()
        while True:
            choice = input("Pick an option: ").strip()
            if choice in picks_list:
                return choice
            else:
                print(f"You need to pick from the list\nThe List: {', '.join(picks_list)}")


    def show_menu(self, choice = "main", *args):
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


    def play_song_from_time(self, file_path, media_player, play_from = 0, random_time = True):
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


    def del_extension(self, song_name: str):
        return song_name[:song_name.rfind(".")] # cut file extension from name (.mp3, .wav,...)


    def play_round(self):
        options = listdir("samples/.")  # get all songs from samples/ folder
        shuffle(options)
        options = options[0:self.answer_count]
        correct_guess = choice(options) # pick random song to play
        
        media_player = Player()
        self.play_song_from_time(f'samples/{correct_guess}', media_player, random_time=True)
        print("Playing random song...")

        options_clean = list(map(self.del_extension, options)) # remove extensions before showing menu
        self.show_menu("songs", *options_clean)
        # print(f"Hint: Pick {correct_guess} to guess right")   # cheat code :d
        guess = int(self.pick_option([str(num + 1) for num in range(self.answer_count)])) - 1 # conver range() to str and decrease 1, 
                                                                                    # because user picks 1-based options

        if correct_guess == options[guess]:
            print("\nGood Job! You guessed right.\n")
            return True
        print("\nNice try, but you didn't guess.\n")
        return False
        

    def play_again(self, score):
        print("\nThe game finished!")
        print(f"Your final score is {score}.")
        if input("Play again? (y)es/(n)o: ").strip().lower() in ["y", "yes"]:
            return True
        return False


    def save_highscore(self, score):
        with open(self.score_file_name, 'a') as file:
            name = input("What's your name?: ")
            file.write(f"\n{name},{str(score)}")
        
        print("Highscore successfully saved")


    def game(self):
        new_game = True
        
        while new_game:
            score = 0
            for _ in range(self.round_count):
                if (self.play_round()):
                    score += 1

            if not path.exists(path.join(self.CURR_PATH, self.score_file_name)):
                print("File missing. Creating new one...")
                self.create_highscore_csv()
            self.save_highscore(score)
            
            new_game = self.play_again(score)


    def add_song(self):
        src = filedialog.askopenfilename()
        dst = r"C:\Users\botcho\Desktop\Projects\Py Stuff\SongMatcher\samples" + "\\" + src.split("/")[-1]    # Take the name of the song
        print(dst)
        time.sleep(1)
        if path.isfile(src):
            copyfile(src, dst)
            print("Song added successfully!")
        else:
            print("No song added.")


    def load_highscore(self):
        print("Reading Highscores\n")
        scores = []

        with open(self.score_file_name, "r") as score_file:  # read highscores file
            score_csv = DictReader(score_file)
            for row in score_csv:
                scores.append(row.values())
        return scores


    def create_highscore_csv(self):
        with open(self.score_file_name, "w") as file:
            file.write(",".join(self.score_header))


    def highscore(self):
        if path.isfile(self.score_file_name):                            # if file exists
            scores = self.load_highscore()  # get highscore data
            print(tabulate(scores, self.score_header))                   # pretty print

        else:   # if file doesn't exist
            print("Doesn't exist. \nCreating highscore file...")
            self.create_highscore_csv()


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
        options = ["a", "b", "c", "q"]
        root = tk.Tk()  # used to open file dialog
        root.withdraw()

        while True:
            choice = self.pick_option(options, "main")
            if choice == options[0]:    # a
                self.game()
            elif choice == options[1]:  # b
                self.add_song()
            elif choice == options[2]:  # c
                self.highscore()
            elif choice == options[3]:  # q
                break


if __name__ == "__main__":
    SongMatcherGame(round_count=5, answer_count=4).main()