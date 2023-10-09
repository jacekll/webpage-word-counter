import pytest

from iterables import ChunkedIterable, ChunkedIterator
from iterables_algo import strip_comments, find_first_pattern_index


@pytest.mark.parametrize("text, expected_text", [
    ("", ""),
    ("a", "a"),
    ("ab", "ab"),
    ("<!-- a --> b", " b"),
    ("<!-- abc -->", ""),
    ("a <!-- abc -->", "a "),
    (" x <!-- abc --> y <!-- de --> z", " x  y  z"),
    ("x<!-- abc -->y<!-- de -->", "xy"),
    ("x<!-- abc --><!-- de -->y", "xy"),
    ("x<!-- abc <!-- -->y<!-- de > -->z", "xyz"),
])
def test_strip_comments(text, expected_text):
    assert "".join([c for c in strip_comments(text)]) == expected_text


@pytest.mark.parametrize("text, pattern, chunks, expected_result", [
    ("a", "a", [], 0),
    ("a", "b", [], -1),
    ("ab", "ab", [], 0),
    ("cab", "ab", [], 1),
    ("cab", "ca", [], 0),
    ("ab", "ac", [], -1),
    ("abc", "ab", [(0, 1)], 0),
    ("abc", "ab", [(0, 2)], 0),
    ("abc", "ab", [(0, 0)], -1),

    ("abcd", "bc", [(0, 1)], -1),

    ("abcd", "bc", [(0, 3)], 1),
    ("abcd", "cd", [(0, 3)], 2),
])
def test_find_first_pattern_index(text, pattern, chunks, expected_result):
    chunked = ChunkedIterable(text)
    for chunk in chunks:
        chunked.add_chunk(chunk[0], chunk[1])
    chunked_iterator: ChunkedIterator = iter(chunked)
    assert find_first_pattern_index(chunked_iterator, pattern) == expected_result
