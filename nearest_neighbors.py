import argparse
import pickle
import os
import random

from db_mgmt.db_mgmt import DatabaseManager
from db_mgmt.db_mgmt import Poetry
from features.size_features import NumLines, NumWords, WidthInChar, WordSize
from features.vocabulary_features import RepetitionScore, ObscurityScore
from features.linguistic_features import SentenceScore
from pony import orm


all_features = [NumLines(), NumWords(), WidthInChar(), WordSize(),
                RepetitionScore(), ObscurityScore(), SentenceScore()]


def _sd(data):
    """Return sum of square deviations of sequence data."""
    c = sum(data) * 1.0 / len(data)
    ss = sum((x - c)**2 for x in data) * 1.0 / len(data)
    return ss**0.5


def _normalize(feature_vals):
    """
    Return normalized list of values.

    normalized value = (value - mean) / range
    """
    # normalize a vector of features
    mu = sum(feature_vals) * 1.0 / len(feature_vals)
    # st_dev = _sd(feature_vals)
    f_range = max(feature_vals) - min(feature_vals)

    res = [ (f - mu) / f_range for f in feature_vals]
    return res


def _dist(v1, v2):
    return sum([ (v1_i - v2_i)**2 for v1_i, v2_i in zip(v1, v2) ])**0.5


@orm.db_session
def nearest_neighbors(n):
    """
    Return dictionary of n nearest neighbors for each poem. e.g.

    nearest_n = {
        poem_id: [(dist, other_poem_id), (dist, some_other_poem_id), ... ]
    }

    Where n is the length of the list.
    """
    poems = [p.to_dict() for p in Poetry.select()]

    feature_names = [f.get_name() for f in all_features]

    poem_data = [[p['id']] + [p.get(f) for f in feature_names] for p in poems]
    ids_features = list(zip(*poem_data))
    ids = ids_features[0]
    feature_cols = ids_features[1:]

    normalized_feature_cols = [_normalize(f) for f in feature_cols]
    normalized_features = list(zip(*normalized_feature_cols))

    nearest_n = {}
    for c, idx, v in zip(range(2**20), ids, normalized_features):
        if c % 100 == 0:
            print("count:", c)

        scores = sorted([
            (_dist(v, v_other), idx_other)
            for (idx_other, v_other)
            in zip(ids, normalized_features)
            if idx_other != idx
        ])

        nearest_n[idx] = scores[:n]

    return nearest_n


@orm.db_session
def update_close_poem(results):
    """
    Update the close_poem index in the database using a results dictionary.

    results = {
        poem_id: [(dist, other_poem_id), (dist, some_other_poem_id), ... ]
    }

    Returns nothing.
    """
    for key, value in results.items():
        db_poem = Poetry[key]
        db_poem.close_poem = value[0][1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find nearest neighbor for all\
                                     poems.')
    parser.add_argument('-r', '--run', action='store_true',
                        help='force run nearest neighbor even if pickled results\
                        is found at temp/nearest_neighbor.p')
    parser.add_argument('-u', '--update', action='store_true',
                        help='update close_poem in database')

    try:
        args = parser.parse_args()
        db_manager = DatabaseManager()

        if not os.path.isdir('temp'):
            os.path.mkdir('temp')

        if not os.path.isfile('temp/nearest_neighbor.p') or args.run:
            res = nearest_neighbors(10)
            pickle.dump(res, open('temp/nearest_neighbor.p', 'wb'))
        else:
            res = pickle.load(open('temp/nearest_neighbor.p', 'rb'))

        if args.update:
            update_close_poem(res)

        i = random.randint(0, 4000)
        vals = res[i]

        print("POEM ID: ", i)
        print("POEM:\n", db_manager.get_poem(i)['poem'])
        print("CLOSE POEM ID: ", vals[0][1])
        print("CLOSE POEM:\n", db_manager.get_poem(vals[0][1])['poem'])

    except KeyboardInterrupt:
            print("Hey there, I see you want to stop.")

    # print("compare!")
    # print(res[1])  # [(0.0018405363693838736, 4735), (0.002961621863987702, 3777), (0.003031168969311884, 4402), (0.0030491674081533178, 1976), (0.0031528731625999184, 4494), (0.003181975820665979, 1524), (0.003258518616697146, 2990), (0.0036164879172037095, 1231), (0.0036283852790374525, 4601), (0.0038571368116782348, 654)]
    # print(res[2])  # [(0.0013935087788747257, 4408), (0.001703174191049602, 4449), (0.00218977398581214, 2277), (0.002264220543154335, 2083), (0.0024170972189330093, 4306), (0.002433450937285613, 3995), (0.002567017781737919, 2740), (0.002571965993149896, 106), (0.0025872318207989203, 3470), (0.0026192235153393436, 1429)]
    # print(res[7])  # [(0.007176315815095065, 476), (0.009305676450038524, 2520), (0.012194491653009664, 4557), (0.01231593551271344, 3049), (0.012527426221016807, 2363), (0.012678252441080982, 977), (0.01327887467413984, 3578), (0.013282592851246921, 340), (0.014009083644914471, 3583), (0.01421927529909832, 1935)]
