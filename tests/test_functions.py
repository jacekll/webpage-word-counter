import pytest

from count_words import strip_comments, strip_tags, get_words


@pytest.mark.parametrize("html, expected_result", [
    ("", ""),
    ("abc", "abc"),
    ("<!-- abc -->", ""),
    ("a <!-- bc --> d", "a  d"),
    ("a <!-- bc\n--> d", "a  d"),
    (
            "<!doctype html><html><head></head><body> a <!-- bc\n--> d</body></html>",
            "<!doctype html><html><head></head><body> a  d</body></html>"
     ),
]
)
def test_strip_comments(html, expected_result):
    assert expected_result == "".join(strip_comments(html))


@pytest.mark.parametrize("html, expected_result", [
    ([
         "<script nonce=\"nzzcBJAQZz901LZCOQeOqQ\">(function(){var src='/images/nav_logo229.png';var iesg=false;document.body.onload = function(){window.n && window.n();if (document.images){new Image().src=src;}\nif (!iesg){document.f&&document.f.q.focus();document.gbqf&&document.gbqf.q.focus();}\n}\n})();</script> abc"],
     "abc"),
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
    ([""], []),
    ([" "], []),
    (["a"], ["a"]),
    (["a "], ["a"]),
    ([" a"], ["a"]),
    ([" a "], ["a"]),
    (["a b"], ["a", "b"]),
    (["ad bc"], ["ad", "bc"]),
    (["ad  bc "], ["ad", "bc"]),
    (["żó  łĆ "], ["żó", "łć"]),
])
def test_get_words(text, expected_result):
    assert list(get_words(text)) == expected_result