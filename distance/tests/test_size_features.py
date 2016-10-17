from distance import size_features

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


def test_get_num_lines():
    expected = float(15)
    actual = size_features.get_num_lines(poem1)
    assert expected == actual


def test_get_num_words():
    expected = float(14 + 20 + 32)
    actual = size_features.get_num_words(poem1)
    assert expected == actual
