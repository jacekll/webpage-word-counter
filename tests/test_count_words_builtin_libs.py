from collections import Counter

from count_words_builtin_libs import WordCountingHTMLParser


def test_count_human_readable_words_in_webpage():
    word_counter = Counter()
    parser = WordCountingHTMLParser(word_counter)
    with open('data/test_simple_htmlentities.html', 'rb') as f:
        text = f.read().decode("UTF-8")

        parser.feed(text)

    assert [('szukaj', 1), ('companyname', 1)] == word_counter.most_common(1000)
