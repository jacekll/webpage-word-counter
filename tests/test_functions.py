import pytest

from count_words import strip_comments, strip_tags, get_words


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
    ([""], ""),
    (["a<br>c"], "a c"),
    (["<br>ab"], "ab"),
    (["<br>ab<br>"], "ab"),
    (["<br>ab<br> c"], "ab  c"),
    (["<img src=\"blah.png\">ab c"], "ab c"),
    (["<img src=\"blah.png\" />ab c"], "ab c"),
    (["<span>ab c </span>"], "ab c "),
    (["<span>ab c </span> "], "ab c  "),
    (["<span>ab c", "</span> d"], "ab c  d"),
    (["<span>ab c", "<span>x</span> d"], "ab c x  d"),
    (["<meta name=\"blah\">ab c"], "ab c"),
    (["<META name=\"blah\" />ab c"], "ab c"),
    (["<html>\n<head><META name=\"blah\" /></head><body>ab c</body></html>"], "ab c"),
]
)
def test_strip_tags(html, expected_result):
    assert "".join(strip_tags(html)).strip() == expected_result.strip()


@pytest.mark.parametrize("text, expected_result", [
    ("", []),
    (" ", []),
    ("a", ["a"]),
    ("a ", ["a"]),
    (" a", ["a"]),
    (" a ", ["a"]),
    ("a b", ["a", "b"]),
    ("ad bc", ["ad", "bc"]),
    ("ad  bc ", ["ad", "bc"]),
    ("żó  łĆ ", ["żó", "łć"]),
])
def test_get_words(text, expected_result):
    assert list(get_words(text)) == expected_result