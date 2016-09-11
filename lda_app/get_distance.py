

def get_distance(doc1, doc2, model):
    '''
    Returns the distance between two documents based on the lda model.

    :param doc1: int (index reference for docs)
    :param doc2: int (index reference for docs)
    :param model: lda output
    :return: float
    '''

    topics1 = model.doc_topic_[doc1]
    topics2 = model.doc_topic_[doc2]

    rms = 0
    for i in range(len(topics1)):
        rms += (topics1[i] - topics2[i])**2

    print(topics1)
    print(topics2)
    print(rms)

    return rms
