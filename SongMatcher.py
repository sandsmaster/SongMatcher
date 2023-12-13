from pyglet.media import Player, load
import asyncio.futures
from random import randint, shuffle, choice
from os import listdir


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
    ANSWER_COUNT = 3
    options = [(r"samples/" + song) for song in listdir("samples/.")]  # get all songs with "samples/" infront of them
    correct_guess = choice(options) # pick random song to play

    play_song_from_time(media_player, correct_guess, random_time=True)
    print(f"Total Song Duration: {media_player.source.duration:.2F} seconds")
    print("Playing random part...")

    shuffle(options)
    show_menu("songs", *options)
    
    guess = int(pick_option([str(num + 1) for num in range(ANSWER_COUNT)])) - 1 # conver range() to str and decrease 1, 
                                                                                # because user doesn't pick 0-based options

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
        print('''The rules are simple. You have to guess the song. 
            Press Enter when you are ready to answear.
            You have 1-30 seconds to guess the song''')

        player = Player()
        for round_num in range(3):
            if (play_round(player)):
                score += 1
        new_game = play_again(score)


def add_song():
    pass


def highscore():
    pass


def main():
    options = ["a", "b", "c"]
    choice = pick_option(options, "main")
    if choice == options[0]:
        game()
    elif choice == options[1]:
        add_song()
    elif choice == options[2]:
        highscore()



if __name__ == "__main__":
    main()