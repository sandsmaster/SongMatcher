from SongMatcher import SongMatcherGame, del_extension, is_correct_guess, sort_scores
from pyglet.media import Player
from pytest import raises


def test_base_del_extension():
    assert del_extension("Hello.mp3") == "Hello"
    assert del_extension("Hello.wav") == "Hello"
    assert del_extension("Hello.man.wav") == "Hello.man"


def test_type_del_extension():
    with raises(TypeError):
        assert del_extension(1)
        assert del_extension(None)


def test_format_del_extension():
    with raises(IndexError):
        assert del_extension("Hello")
        assert del_extension("Hi My Friends.")


def test_is_correct_guess():
    assert is_correct_guess("Hi", "Hi") == True
    assert is_correct_guess("Hi", "Why") == False
    assert is_correct_guess("Pi thon", "pi thon") == False


def test_base_sort_scores():
    scores_f = [            # scores False
        ["Mick", 20],
        ["Don", 10],
        ["Boney", 12]
    ]
    scores_t = [            # scores True (sorted successfully)
        ["Mick", 20],
        ["Boney", 12],
        ["Don", 10]
    ]                
    assert sort_scores(scores_f, 1) == scores_t

    scores_f[0] = ["Mick", 3]  # set Mick's score to 3
    scores_t = [
        ["Boney", 12],
        ["Don", 10],
        ["Mick", 3]
    ]
    assert sort_scores(scores_f, 1) == scores_t


def test_type_sort_scores():
    with raises(TypeError):
        assert sort_scores(10, 1)
        assert sort_scores(False, 1)
        assert sort_scores(["No list"], 1)


def test_empty_sort_scores():
    with raises(IndexError):
        assert sort_scores([], 1)

                                                       
def test_len_get_songs():
    assert len(SongMatcherGame(3, 3).get_songs()) == 3
    assert len(SongMatcherGame(3, 1).get_songs()) == 1

def test_type_get_songs():
    assert type(SongMatcherGame(3, 3).get_songs()[0]) == str


class TestSongMatcherGame:
    game_obj = SongMatcherGame(3, 3)
    player_obj = Player()

    def test_choice_show_menu(self):
        with raises(NameError):
            assert self.game_obj.show_menu("ok")
            assert self.game_obj.show_menu(1)
            assert self.game_obj.show_menu([])

    def test_play_song_from_time_check_par_type(self):
        with raises(TypeError):
            assert self.game_obj.play_song_from_time_check_par_type(20, self.player_obj, 0, True)
            assert self.game_obj.play_song_from_time_check_par_type("C:\\Users\\me\\Desktop", "Insert player here", 0, True)
            assert self.game_obj.play_song_from_time_check_par_type("C:\\Users\\me\\Desktop", self.player_obj, "start time", True)
            assert self.game_obj.play_song_from_time_check_par_type("C:\\Users\\me\\Desktop", self.player_obj, 0, "True")