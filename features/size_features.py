from features.feature_extractor import FeatureExtractor

import re


class NumLines(FeatureExtractor):
    '''The number of lines in the poem.'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'num_lines')

    def get_feature(self, poem):
        strip_poem = poem['poem'].strip('\n')
        split_poem = strip_poem.split('\n')
        if len(split_poem) == 0:
            self.print_poem_info(poem)
            raise AttributeError('Poem of 0 lines...')
        return len(split_poem)


class NumWords(FeatureExtractor):
    '''The number of words in the poem.'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'num_words')

    def get_feature(self, poem):
        x = re.sub('\n+', ' ', poem['poem']).strip().split(' ')
        return len(x)


class WidthInChar(FeatureExtractor):
    '''Average line length in characters.'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'width_in_char')

    def get_feature(self, poem):
        lines = poem['poem'].split('\n')
        legit_lines = [l for l in lines if len(l) != 0]
        len_lines = [len(l) for l in legit_lines]
        if len(len_lines) == 0:
            self.print_poem_info(poem)
            raise AttributeError('Poem of 0 lines...')
        return float(sum(len_lines)) / len(len_lines)


class WordSize(FeatureExtractor):
    '''Mean word length in characters.'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'word_size')

    def get_feature(self, poem):
        words = re.split('\n| ', poem['poem'])
        words = [w for w in words if w != '']
        lengths = [len(w) for w in words]
        return sum(lengths) / len(lengths)
