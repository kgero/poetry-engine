from features.feature_extractor import FeatureExtractor

import re


class NumLines(FeatureExtractor):
    '''The number of lines in the poem.'''

    def get_feature(self, poem):
        return len(poem['poem'].split('\n')) - 1


class NumWords(FeatureExtractor):
    '''The number of words in the poem.'''

    def get_feature(self, poem):
        x = re.sub('\n+', ' ', poem['poem']).strip().split(' ')
        return len(x)


class CharWidth(FeatureExtractor):
    '''Average line length in characters.'''

    def get_feature(self, poem):
        lines = poem['poem'].split('\n')
        legit_lines = [l for l in lines if len(l) != 0]
        len_lines = [len(l) for l in legit_lines]
        return float(sum(len_lines)) / len(len_lines)


class WordSize(FeatureExtractor):
    '''Mean word length in characters.'''

    def get_feature(self, poem):
        words = re.split('\n| ', poem['poem'])
        words = [w for w in words if w != '']
        lengths = [len(w) for w in words]
        return sum(lengths) / len(lengths)
