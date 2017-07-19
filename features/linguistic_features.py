from features.feature_extractor import FeatureExtractor

import re

class SentenceScore(FeatureExtractor):
    '''How much a poem uses sentences (in a prosaic way.)'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'sentence_score')

    def get_feature(self, poem):
        '''Accumulates score for good grammar.

        +1 For each sentence used.
        (Sentence ends with period.)
        +1 For each sentence starting with a capital letter.
        +1 For each sentence that ends with line break.

        Divide score by number of characters in poem.
        Multiply by ten to get larger numbers.
        Clearly this favors lots of short sentences. So be it.
        '''
        score = self.get_score(poem)

        return score * 10 / len(poem['poem'])


    def get_score(self, poem):
        score = 0
        sentences = poem['poem'].split('.')
        sentences = [s for s in sentences if re.search('[a-zA-Z]', s)]
        score += len(sentences)

        linebreak_sentences = [s for s in sentences if s[0] == '\n']
        score += len(linebreak_sentences)

        capital_sentences = [s for s in sentences if s.strip()[0].isupper()]
        score += len(capital_sentences)

        return score


class EmjambmentScore(FeatureExtractor):
    '''How much a poem uses emjambment.'''
