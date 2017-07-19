from features.linguistic_features import SentenceScore


def test_sentence_score():
    feat = SentenceScore()

    text = "Single good sentence."
    poem = {'poem': text}
    score = feat.get_score(poem)
    assert score == 2
    feature = feat.get_feature(poem)
    assert feature == 2 * 10 / 21

    text = "Two great sentences, here. And here."
    poem = {'poem': text}
    score = feat.get_score(poem)
    assert score == 4

    text = "Two great sentences, here.\nAnd here."
    poem = {'poem': text}
    score = feat.get_score(poem)
    assert score == 5
