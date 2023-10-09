from count_words import get_words, count_words, skip_doctype, strip_comments, strip_tags


def test_count_words_simple_script():
    with open('../test_simple_utf8.html', 'rb') as f:
        text = f.read().decode("UTF-8")

    assert [()] == count_words(
        get_words(
            strip_tags(
                strip_comments(
                    skip_doctype(text)
                )
            )
        )
    )
