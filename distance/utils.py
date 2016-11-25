
def normalize_feature(feature):
    '''
    Return normalized feature.

    :param feature: list of floats
    :return: list of floats
    '''
    u = sum(feature) / float(len(feature))
    r = max(feature) - min(feature)
    normalized = []
    for val in feature:
        n_val = (val - u) / r
        normalized.append(n_val)
    return normalized


def normalize_element(element, u, r):
    '''
    Return normalized element.

    :param element: int or float
    :param u: int or float
    :param r: int or float
    :return: float
    '''
    return (element - float(u)) / float(r)


def get_norm_attr(feature):
    '''
    Return dictionary of normalization attributes. e.g.
    {"mean": 3.5, "range": 100}

    :param feature: list of floats
    :return: dictionary
    '''
    u = sum(feature) / float(len(feature))
    r = max(feature) - min(feature)
    d = {"mean": u, "range": r}
    return d
