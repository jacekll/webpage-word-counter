from collections import Counter

import pytest

from count_words import get_words, strip_comments, strip_tags, get_top_n_words
from main import MyHTMLParser


@pytest.mark.parametrize("filename", [
    "test_simple.html",
    "test_comments.html",
])
def test_count_words_simple(filename: str):
    with open(f'data/{filename}', 'rb') as f:
        text = f.read().decode("UTF-8")
    result = get_top_n_words(
        get_words(
            strip_tags(
                strip_comments(
                    text
                )
            )
        ),
        1000
    )

    word_counter = Counter()
    parser = MyHTMLParser(word_counter)
    parser.feed(text)

    assert set(result) == set(word_counter.most_common())


@pytest.mark.parametrize("filename, expected_result", [
    ("test_javascript.html", {("żółć", 1)}),
    ("test_simple_htmlentities.html", {
        ('companyname', 1),
        ('szukaj', 1),
    }
     ),
])
def test_count_words_advanced(filename: str, expected_result):
    with open(f'data/{filename}', 'rb') as f:
        text = f.read().decode("UTF-8")
    result = get_top_n_words(
        get_words(
            strip_tags(
                strip_comments(
                    text
                )
            )
        ),
        1000
    )
    assert set(result) == expected_result
