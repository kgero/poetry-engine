import lda
import pickle

from lda_app.create_docs import get_docs


def run_lda(root_path, n_topics=20, n_iter=1500):
    '''
    Returns documents and model.
    documents = (docs, vocab, titles, poets, urls)
    model = lda_model

    :param root_path: str (path to root of poems directory)
    :param n_topics: int
    :param n_iter: int
    :return: (documemnts, model)
    '''

    docs, vocab, titles, poets, urls = get_docs("poems")

    print('Document dimensions:')
    print(docs.shape)

    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1)
    model.fit(docs)

    documents = (docs, vocab, titles, poets, urls)
    pickle.dump(documents, open("temp/documents.p", "wb"))
    pickle.dump(model, open("temp/model.p", "wb"))

    return documents, model
