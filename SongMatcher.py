from pyglet.media import Player, load
import asyncio.futures
from random import randint, shuffle, choice
from os import listdir, path
from shutil import copyfile


def pick_option(picks_list, menu_arg = None):
    if menu_arg:
        show_menu()
    # with asyncio.futures.ThreadPoolExecutor() as executor:
    #     pass
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
    ANSWER_COUNT = 3
    options = listdir("samples/.")  # get all songs with "samples/" infront of them
    shuffle(options)
    options = options[0:3]
    correct_guess = choice(options) # pick random song to play
    
    media_player = Player()
    play_song_from_time(f'samples/{correct_guess}', media_player, random_time=True)
    print("Playing random part...")

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


def game():
    new_game = True
    while new_game:
        score = 0
        for round_num in range(3):
            if (play_round()):
                score += 1
        new_game = play_again(score)


def add_song():
    dst = r"C:\Users\botcho\Desktop\Projects\Py Stuff\SongMatcher\samples"
    src = input("Please enter song path. [Exit]").strip()
    while not path.isfile(src) and not (src.lower() in ["e", "exit", "quit"]):
        # while file isn't found and user doesn't want to exit 
        print("This is not a valid file. Please try again!")
        src = input("Please enter song path").strip()
    copyfile(src, dst)


def highscore():
    pass


def main():
    options = ["a", "b", "c", "q"]
    while True:
        choice = pick_option(options, "main")
        if choice == options[0]:
            game()
        elif choice == options[1]:
            add_song()
        elif choice == options[2]:
            highscore()
        elif choice == options[3]:
            break


if __name__ == "__main__":
    main()