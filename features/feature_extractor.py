
class FeatureExtractor:
    '''
    Base class, don't instatiate this class directly.
    '''
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def print_poem_info(self, poem):
        '''
        Print information about the poem.

        :dict poem: Dictionary with elements id, title, poem
        :return: None
        '''
        print("ID: {}, TITLE: {}, POEM: {}".format(poem['id'], 
                poem['title'], poem['poem']))

    def get_feature(self, poem):
        '''
        Returns the feature.

        :dict poem: Dictionary with elements title, poet, poem
        :return: int or bool
        '''
        raise NotImplementedError
