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
    ("test_simple_utf8.html", {
        ('com', 1),
        ('dla', 1),
        ('dysk', 1),
        ('firm', 1),
        ('gdzie', 1),
        ('gmail', 1),
        ('google', 2),
        ('grafika', 1),
        ('głosować', 1),
        ('historia', 1),
        ('mapy', 1),
        ('o', 1),
        ('odbędą', 1),
        ('online', 1),
        ('października', 1),
        ('play', 1),
        ('prywatność', 1),
        ('reklamuj', 1),
        ('rozwiązania', 1),
        ('się', 3),
        ('sprawdź', 1),
        ('szukaj', 1),
        ('szukanie', 1),
        ('ustawienia', 1),
        ('warunki', 1),
        ('wiadomości', 1),
        ('więcej', 1),
        ('wszystko', 1),
        ('wybory', 1),
        ('youtube', 1),
        ('zaawansowane', 1),
        ('zaloguj', 1)
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
