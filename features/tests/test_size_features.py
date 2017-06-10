from features.size_features import NumLines, NumWords, CharWidth, WordSize

poem1 = "Does not mean silence.\n\
The absence of moon in the day sky\n\
for example.\n\
\n\
Does not mean barely to speak,\n\
the way a child's whisper\n\
makes only warm air\n\
on his mother's right ear.\n\
\n\
To play pianissimo\n\
is to carry sweet words\n\
to the old woman in the last dark row\n\
who cannot hear anything else,\n\
and to lay them across her lap like a shawl.\n\
\n"

poem = {'poem': poem1}


def test_num_lines():
    feat = NumLines("NumLines")
    assert feat.get_feature(poem) == 15


def test_num_words():
    feat = NumWords("NumWords")
    assert feat.get_feature(poem) == 14 + 20 + 32


def test_char_width():
    feat = CharWidth("CharWidth")
    assert feat.get_feature(poem) == 26.666666666666668


def test_word_size():
    feat = WordSize("WordSize")
    assert feat.get_feature(poem) == 4.03030303030303
