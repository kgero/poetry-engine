from distance import utils


def get_lda_distance(model, docs):
    '''
    Return list of poems indeces and list of normalized rms distances.

    :param model: lda model
    :param docs: lda docs
    :return: list of tuples, list of floats
    '''
    indeces = []
    rms_distance = []
    # python arrays/lists are indexed at 0, but the db indexes at 1
    # so i and j are python indexes, but we plus one bc we want the db index
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            rms = lda_distance(i, j, model)
            indeces.append((i + 1, j + 1))
            rms_distance.append(rms)

    return indeces, utils.normalize_feature(rms_distance)


def lda_distance(doc1, doc2, model, printout=False):
    '''
    Return the distance between two documents based on the lda model.

    :param doc1: int (index reference for docs)
    :param doc2: int (index reference for docs)
    :param model: lda output
    :param printout: bool
    :return: float
    '''

    topics1 = model.doc_topic_[doc1]
    topics2 = model.doc_topic_[doc2]

    rms = 0
    for i in range(len(topics1)):
        rms += (topics1[i] - topics2[i])**2

    if printout:
        print(topics1)
        print(topics2)
        print(rms)

    return rms


def find_closest_doc(doc1, indeces, lda_d, size_d):
    '''
    Return index of closest documents to doc1 based on get_distance.

    :param doc1: int (index reference for base document)
    :param indeces: list of tuples, each of two poem indeces (i.e. a relation)
    :param lda_d: list of floats, corresponding to lda distance between poems
    :param size_d: list of floats, corresponding to size distance between poems
    :return: integer index of closest poem
    '''

    return None


def get_distance(lda_d, size_d, l):
    '''
    Return distance as a function of the lda and size distance.

    :param lda_d: float
    :param size_d: float
    :param l: float, weight for lda_d between 0 and 1
    :return: float
    '''
    return None

def insert_rms(close_docs, close_rms, doc, rms):
    '''
    Insert doc and rms into lists such that rms is decreasing w index
    and the lists do no change length, i.e. removes largest entry.

    :param close_docs: list
    :param close_rms: list
    :param doc: int
    :param rms: float
    :return: None
    '''
    if rms > close_rms[0]:
        return None
    for i in range(len(close_rms)):
        if rms > close_rms[i]:
            close_rms.insert(i, rms)
            close_rms.pop(0)
            close_docs.insert(i, doc)
            close_docs.pop(0)
            return None
    close_rms.append(rms)
    close_rms.pop(0)
    close_docs.append(doc)
    close_docs.pop(0)
