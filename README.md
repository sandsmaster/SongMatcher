 # SongMatcher
#### Video Demo:  <URL HERE>
#### Description:

This is a game, made to play songs for you and let you guess their titles.
Some of the main functions added are adding new songs and recording highscores in a CSV file, but
this is just a brief overview of the program itself. Let's begin with the details

## The Game (project.py):

Starting with the structure, A class to house most functions in the game is used, so there aren't many
standalone functions. This helps house a few important properties. Here's how the structure looks like:
```
class SongMatcherGame():
    CURR_PATH = path.abspath(r'.')    
    score_file_name = "highscore.csv"
    score_header = ["Player", "Score"]
    root = tk.Tk()  # used to open file dialog
```

When you start the game, you are met with the main menu. 
It looks like this:

![Picture of the main menu](/doc%20images/main_menu.png)

Here a function `pick_option()` takes the players choice 
and prevent other input. Also the package [__colorama__](https://pypi.org/project/colorama/) is used to 
add some color to the game.

### Play Game:

If you pick the first option, the game loop starts. Number of rounds and number of options is specified when creting the `SongMatcherGame` class in the `main()` function.

First thing is reading and shuffling all the songs from the ***/samples*** folder, where all used songs are stored. Then the list is trimmed to `self.answer_count` and the correct guess is picked. If ***/samples*** is empty, the game displays a message.

Next ***Player()*** object is created with `pyglet` and song is played from random timestamp. Additional function is added inside the 
`play_song_from_time()` function to check, if the parameters are valid.

Cleaning and displaying the options follows. Here's an image of the round menu:

![Image of the round menu](/doc%20images/round_menu.png)

After picking a song, the program checks if player's choice is correct. Then the score increases, if there was a correct guess. A check for the ***highscores.csv*** is performed. If file is found, the user is asked for a name to be saved with. If no name suplied, the save is skipped. 

Finally, the game asks the player, if they want to play again. Here's what it looks like:

![Image of play again prompt](/doc%20images/repeat_prompt.png)

### Add a Song:

A file explorer shows up and asks the user for songs to pick. After that displays a message wether it was successful. The file dialog is created by [Tk](https://docs.python.org/3/library/tkinter.html)

### Highscores:

The highscores option calls a sorting function and displays the contents of `highscore.csv` via a tabulate function from [tabulate](https://pypi.org/project/tabulate/), sorted by the score. If the file doesn't exist, a new one is created. The headers are included on creation. Also, thanks to the [csv's](https://docs.python.org/3/library/csv.html) ***DictReader*** the apostrophe (`'`) symbol is supported. This is how it looks like:

Here's how the highscore looks like:

![Highscore image](/doc%20images/highscore.png)

### Settings

The game has a settings menu as well. Currently it looks like this:

![Settings image](/doc%20images/settings.png)

You can set the number of rounds and possible answers to pick from.

Also there's type and range checking. Rounds must be more than 0. Answers must be more than 1

### Error Handling

If you pass in a wrong option, when you are given a choice, you will get reminded you can't pick that one.
The most basic example of this is with picking an option in the main menu. 

Picking the incorrect one will display a warning. See below:

![Main menu error handling](./doc%20images/main_menu_error.png)

When changing the settings in the settings menu, you also get these warnings:
- Non-string input - "You need to pick a NUMBER. This isn't one"
- Round count too low - "Number must be bigger than 0"
- Answer count too low - "Number must be bigger than 1"

The script checks for the samples folder and highscore.csv file as well, to make sure they exist. If they don't, they are created by the program. 

Samples folder not found error:

![Samples folder not found error message](./doc%20images/samples_not_exist_error.png)

Highscore.csv file not found error:

![Highscore.csv file not found error message](./doc%20images/highscore_not_exist_error.png)

There is also a check for songs, inside of the samples folder. If none are found, an error shows up:

![No songs error message](./doc%20images/no_songs_found_error.png)

### Miscellaneous:

Additional functions are:
- ***wait_user()*** - waits for user input. Useful when output needs to stay visible, so the user has time to read it
- ***clear_scr()*** - clears the screen. Uses character escape codes. You can see the code below
```
def clear_scr(self):
    print("\033[H\033[J", end="")
```

## Testing (test_project.py)

Here We test both the stand-alone functions
```
del_extension()
is_correct_guess()
sort_scores()
```
And methods from `SongMatcherGame`
```
get_songs()
show_menu()
play_song_from_time_check_par_type()
play_again()
```

A special test class is written to house instance of `SongMatcherGame`, to make testing easier.

For `del_extension` the following cases were tested
- Expected Input
- Wrong Type
- Wrong Format

For `is_correct_guess` the following cases were tested
- Expected input

For `sort_scores` the following cases were tested
- Expected Input
- Wrong Type
- Empty List of Scores

For `get_songs` the following cases were tested
- List Length
- List Type

For `choice_show_menu` the following cases were tested
- Expected Output

For `play_song_from_time_check_par_type` the following cases were tested
- Expected Output

For `correct_guess` the following cases were tested
- Expected Output

## Miscellaneous

There are a few other files added to the project. Some are automatically generated from VSCode and others are added manually

### Git Ignore File

The git ignore file marks all the files, that are not part of the code.

These are:
- samples folder (and all the sample songs inside)
- highscore.csv
- .venv (virtual environment)
- VSCode generated files

### Game Plan

This is a file with basic plan and notes for the game, to help make the development easier.

### Doc Images

These are the images, you see in this file