from SongMatcher import SongMatcherGame, del_extension, is_correct_guess, sort_scores


def test_del_extension():
    assert del_extension("Hello.mp3") == "Hello"
    assert del_extension("Hello.wav") == "Hello"
    assert del_extension("Hello.man.wav") == "Hello.man"


def test_is_correct_guess():
    assert is_correct_guess("Hi", "Hi") == True
    assert is_correct_guess("Hi", "Why") == False
    assert is_correct_guess("Pi thon", "pi thon") == False


def test_sort_scores():
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
    assert sort_scores(scores_f) == scores_t

    scores_f[0] = ["Mick", 3]  # set Mick's score to 3
    scores_t = [
        ["Boney", 12],
        ["Don", 10],
        ["Mick", 3]
    ]
    assert sort_scores(scores_f) == scores_t

                                                       
def test_get_songs_len():
    assert len(SongMatcherGame(3, 3).get_songs()) == 3
    assert len(SongMatcherGame(3, 1).get_songs()) == 1

def test_get_songs_type():
    assert type(SongMatcherGame(3, 3).get_songs()[0]) == str