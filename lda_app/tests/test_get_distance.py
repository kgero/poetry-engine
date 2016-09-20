from lda_app.get_distance import insert_rms


def test_insert_rms():
    # With something that should not be inserted
    doc = 4
    rms = 15
    close_docs = [1, 2, 3]
    close_rms = [10, 7, 5]
    insert_rms(close_docs, close_rms, doc, rms)
    expected_close_docs = [1, 2, 3]
    expected_close_rms = [10, 7, 5]
    assert close_docs == expected_close_docs
    assert close_rms == expected_close_rms

    # With val that should be inserted
    doc = 4
    rms = 9
    close_docs = [1, 2, 3]
    close_rms = [10, 7, 5]
    insert_rms(close_docs, close_rms, doc, rms)
    expected_close_docs = [4, 2, 3]
    expected_close_rms = [9, 7, 5]
    assert close_docs == expected_close_docs
    assert close_rms == expected_close_rms

    # With smallest val to be inserted
    doc = 4
    rms = .4
    close_docs = [1, 2, 3]
    close_rms = [.9, .7, .5]
    insert_rms(close_docs, close_rms, doc, rms)
    expected_close_docs = [2, 3, 4]
    expected_close_rms = [.7, .5, .4]
    assert close_docs == expected_close_docs
    assert close_rms == expected_close_rms
