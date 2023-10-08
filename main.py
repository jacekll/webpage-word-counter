from collections import Counter
from urllib import request
from sys import argv
from typing import Iterable, Tuple, Final

import re
from html.parser import HTMLParser

import unicodedata


FIND_WORDS_PATTERN = re.compile(r'[^\W\d]+', re.MULTILINE)


def normalize_word(word: str) -> str:
    return unicodedata.normalize('NFD', unicodedata.normalize('NFD', word).casefold())


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
        if self.started == False or self.finished == True:
            return
        if data == "":
            return
        if self.closest_parent_tag not in self.NON_HUMAN_READABLE_TAGS:
            print("Encountered some text :", data)
            self._counter.update(
                map(
                    normalize_word,
                    FIND_WORDS_PATTERN.findall(data))
            )


def count_human_readable_words_in_webpage(url):
    word_counter = Counter()

    parser = MyHTMLParser(word_counter)
    with request.urlopen(url) as response:
        text = response.read().decode(response.headers.get_content_charset())
        parser.feed(text)

    print(f"{repr(word_counter.most_common(1000))}")
    parser.close()


if __name__ == '__main__':
    count_human_readable_words_in_webpage(argv[1])
