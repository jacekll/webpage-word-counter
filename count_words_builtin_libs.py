import sys
from collections import Counter
from sys import argv
from typing import Iterable, Tuple, Final

import re
from html.parser import HTMLParser

from custom_types import TopNWordsResult
from input_output import display_and_save_top_results, get_page_content

FIND_WORDS_PATTERN = re.compile(r'[^\W\d]+', re.MULTILINE)


def normalize_word(word: str) -> str:
    return word.casefold()


class MyHTMLParser(HTMLParser):
    NON_HUMAN_READABLE_TAGS: Final[set[str]] = {"style", "link", "script", "head", "meta", "title", "html"}
    closest_parent_tag = None
    started = False
    finished = False

    def __init__(self, counter: Counter, **kwargs):
        super().__init__(**kwargs)
        self._counter = counter

    def handle_starttag(self, tag: str, attrs: Iterable[Tuple[str, str]]):
        if tag == 'body':
            self.started = True
        self.closest_parent_tag = tag

    def handle_endtag(self, tag: str):
        if tag == 'body':
            self.finished = True

    def handle_data(self, data: str):
        if self.started is False or self.finished is True:
            return
        if data == "":
            return
        if self.closest_parent_tag not in self.NON_HUMAN_READABLE_TAGS:
            self._counter.update(
                map(
                    normalize_word,
                    FIND_WORDS_PATTERN.findall(data))
            )


def get_top_human_readable_words_in_webpage(url: str, n: int) -> TopNWordsResult:
    word_counter = Counter()
    parser = MyHTMLParser(word_counter)
    text = get_page_content(url)
    parser.feed(text)
    parser.close()
    return word_counter.most_common(n)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {__file__} <url>")
        exit(1)
    display_and_save_top_results(get_top_human_readable_words_in_webpage(argv[1], 10))
