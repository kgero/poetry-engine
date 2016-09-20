

def get_distance(doc1, doc2, model, printout=False):
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


def find_close_docs(doc1, model, num_to_return=10):
    '''
    Return num_to_return closest documents to doc1 based on get_distance.

    :param doc1: int (index reference for docs)
    :param model: lda output
    :param num_to_return: int
    :return: list (of index references for docs), list (of correspond rms vals)
    '''

    close_docs = [0] * num_to_return
    close_rms = [100] * num_to_return

    for doc in range(model.doc_topic_.shape[0]):
        if doc == doc1:
            continue
        rms = get_distance(doc1, doc, model)
        if close_rms[0] > rms:
            insert_rms(close_docs, close_rms, doc, rms)

    return close_docs, close_rms


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
