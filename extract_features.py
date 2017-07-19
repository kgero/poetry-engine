import argparse

from db_mgmt.db_mgmt import DatabaseManager
from db_mgmt.db_mgmt import Poetry
from features.size_features import NumLines, NumWords, WidthInChar, WordSize
from features.vocabulary_features import RepetitionScore, ObscurityScore
from features.linguistic_features import SentenceScore
from pony import orm


all_features = [NumLines(), NumWords(), WidthInChar(), WordSize(),
                RepetitionScore(), ObscurityScore(), SentenceScore()]

@orm.db_session
def extraction(start, stop, overwrite=False):
    db_poems = orm.select(p for p in Poetry).for_update().order_by(Poetry.id)
    for db_poem in db_poems[start:stop]:
        for feature in all_features:
            name = feature.get_name()
            dict_poem = db_poem.to_dict()
            if not dict_poem.get(name) or overwrite:
                value = feature.get_feature(dict_poem)
                db_poem.set(**{name: value})


def extract_all_features(overwrite=False):
    c = 0
    while c < 4864:
        extraction(c, c + 100, overwrite=overwrite)
        print("{} poems done".format(c))
        c += 100


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract poem features!')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='overwrite features in database. default: \
                        if feature already exists, do not calculate again.')
    args = parser.parse_args()

    db_manager = DatabaseManager()
    try:
        extract_all_features(overwrite=args.overwrite)
    except KeyboardInterrupt:
        print("Hey there, I see you want to stop.")
