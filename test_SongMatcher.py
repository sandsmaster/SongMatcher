from SongMatcher import SongMatcherGame


def test_del_extension():
    assert SongMatcherGame(3, 3).del_extension("Hello.mp3") == "Hello"
    assert SongMatcherGame(1, 3).del_extension("Hello.wav") == "Hello"
    assert SongMatcherGame(3, 1).del_extension("Hello.man.wav") == "Hello.man"


def test_get_songs_len():
    assert len(SongMatcherGame(3, 3).get_songs()) == 3
    assert len(SongMatcherGame(3, 1).get_songs()) == 1

def test_get_songs_type():
    assert type(SongMatcherGame(3, 3).get_songs()[0]) == str

def test_is_correct_guess():
    assert SongMatcherGame(3, 3).is_correct_guess("Hi", "Hi") == True