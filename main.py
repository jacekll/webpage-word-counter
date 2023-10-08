import collections
from abc import abstractmethod, ABCMeta
from collections import defaultdict
from typing import Iterable, Tuple, Generator, Optional

import httpx
import re
from html.parser import HTMLParser

import unicodedata


FIND_WORDS_PATTERN = re.compile(r'\w+', re.MULTILINE)


def normalize_word(word: str) -> str:
    return word.lower()


class MyHTMLParser(HTMLParser):
    closest_parent_tag = None
    started = False
    finished = False
    letter_pattern = re.compile(r'\w', re.MULTILINE)

    def __init__(self, counter: collections.Counter, **kwargs):
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
        text_part = unicodedata.normalize("NFC", data)  # https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
        if self.letter_pattern.search(text_part) is None:
            return
        if self.closest_parent_tag not in {"style", "link", "script", "head", "meta", "title", "html"}:
            print("Encountered some text :", text_part)
            self._counter.update(
                map(
                    normalize_word,
                    FIND_WORDS_PATTERN.findall(text_part))
            )


def count_human_readable_words_in_webpage(url):
    word_counter = collections.Counter()

    parser = MyHTMLParser(word_counter)
    with httpx.stream("GET", url) as r:
        for text in r.iter_text():
            parser.feed(text)
            if parser.finished:
                break

    print(f"{repr(word_counter.most_common(1000))}")
    parser.close()


if __name__ == '__main__':
    count_human_readable_words_in_webpage('https://www.google.pl/')
