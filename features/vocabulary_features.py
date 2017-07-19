from features.feature_extractor import FeatureExtractor

from nltk.stem import SnowballStemmer


class RepetitionScore(FeatureExtractor):
    '''A score from 0 to 1 indicating how much repetition is used.'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'repetition_score')
        self.stemmer = SnowballStemmer("english")

    def get_feature(self, poem):
        """
        RepetitionScore is a repscore divided by the number of words.

        For each word in the poem, repscore can be increased once (or not all.)

        repscore += 1 if the word (stripped of punctuation) is seen more than
        once in the poem.

        repscore += 0.5 if the stem of the word is seen more than once.
        """
        poem_text = poem['poem']
        wordlist = [w.rstrip('?:!.,;') for w in poem_text.split(' ')]

        stemlist = [self.stemmer.stem(w) for w in wordlist]

        repscore = 0
        for i in range(len(wordlist)):
            if wordlist.count(wordlist[i]) > 1:
                repscore += 1
            elif stemlist.count(stemlist[i]) > 1:
                repscore += 0.5

        return repscore / len(wordlist)


class ObscurityScore(FeatureExtractor):
    '''A score from 0 to 1 indicating how obscure the vocabulary is.'''

    def __init__(self):
        FeatureExtractor.__init__(self, 'obscurity_score')
        self.common = self.get_wordlist(1000)

    def get_wordlist(self, n):
        """Return list of n top words from word list.

        wordfrequencies.csv is the top 5000 most frequency words in english.
        Columns are: Rank,Word,Part of speech,Frequency,Dispersion
        Source: wordfrequency.info
        """
        filepath = 'features/data/wordfrequencies.csv'

        with open(filepath, 'r') as myfile:
            head = [next(myfile) for x in range(n)]

        commonlist = []
        for line in head:
            commonlist.append(line.split(',')[1].lower())

        return(commonlist)

    def preview_common(self, n):
        """Return list of top n common words."""
        return self.common[:n]

    def get_feature(self, poem):
        """Return % of words in the poem NOT in the top 1000 words."""
        poem_text = poem['poem']
        wordlist = [w.rstrip('?:!.,;').lower() for w in poem_text.split(' ')]
        obscore = 0
        for w in wordlist:
            if w not in self.common:
                obscore += 1

        return obscore / len(wordlist)
