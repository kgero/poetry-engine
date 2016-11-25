from distance.utils import normalize_feature


def test_normalize_feature():
    feature = [0., .5, 1.]
    expected = [-.5, 0, .5]
    actual = normalize_feature(feature)
    assert actual == expected

    feature = [-.5, 0, .5]
    expected = [-.5, 0, .5]
    actual = normalize_feature(feature)
    assert actual == expected
