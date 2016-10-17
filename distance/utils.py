
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
