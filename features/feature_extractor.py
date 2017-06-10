
class FeatureExtractor:
    '''
    Base class, don't instatiate this class directly.
    '''
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_feature(self, poem):
        '''
        Returns the feature.

        :dict poem: Dictionary with elements title, poet, poem
        :return: int or bool
        '''
        raise NotImplementedError
