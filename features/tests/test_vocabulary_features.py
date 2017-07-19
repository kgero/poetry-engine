from features.vocabulary_features import RepetitionScore, ObscurityScore


def test_repetition_score():
    feat = RepetitionScore()

    text = "This has no repetitions."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0

    text = "repeat repeat repeat."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 1

    text = "This has repeat repeat."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0.5

    text = "This this has repeats repeat."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0.4

    text = "This this has repeat repeat."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0.6

    text = "Computing compute computer."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0.5

    text = "Crying cried cry."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0.5


def test_obscurity_score():
    feat = ObscurityScore()

    text = "This most common."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 0

    text = "craziness vocabulary residing here-abouts."
    poem = {'poem': text}
    assert feat.get_feature(poem) == 1
