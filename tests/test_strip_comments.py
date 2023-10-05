import pytest

from count_words import strip_comments, strip_tags


@pytest.mark.parametrize("html, expected_result", [
    ("", ""),
    ("abc", "abc"),
    ("<!-- abc -->", ""),
    ("a <!-- bc --> d", "a  d"),
    ("a <!-- bc\n--> d", "a  d"),
]
)
def test_strip_comments(html, expected_result):
    assert expected_result == "".join(strip_comments(html))


@pytest.mark.parametrize("html, expected_result", [
    ("", ""),
    ("a<br>c", "ac"),
    ("<br>ab", "ab"),
    ("<br>ab<br>", "ab"),
    ("<br>ab<br> c", "ab c"),
    ("<img src=\"blah.png\">ab c", "ab c"),
    ("<img src=\"blah.png\" />ab c", "ab c"),
    ("<span>ab c </span>", "ab c "),
    ("<span>ab c </span> ", "ab c  "),
]
)
def test_strip_tags(html, expected_result):
    assert expected_result == "".join(strip_tags(html))
