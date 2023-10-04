from abc import abstractmethod, ABCMeta
from collections import defaultdict
from typing import Iterable, Tuple, Generator, Optional

import httpx
import re
from html.parser import HTMLParser

import unicodedata


StrGenerator = Generator[str, None, None]

SPLIT_WORDS_PATTERN = re.compile(r'(\W|\s)+', re.MULTILINE)


class IWordCollectionVisitor(metaclass=ABCMeta):
    def __init__(self, next_visitor: Optional["IWordCollectionVisitor"] = None):
        self.next_visitor = next_visitor

    def visit_words(self, words: StrGenerator) -> StrGenerator:
        for word in words:
            if self.next_visitor:
                for next_word in self.next_visitor(word):
                    for w in self.visit(next_word):
                        yield w
            else:
                for w in self.visit(word):
                    yield w

    @abstractmethod
    def visit(self, word: str) -> StrGenerator:
        ...


class WordNormalizer(IWordCollectionVisitor):
    def visit(self, word: str) -> StrGenerator:
        yield word.lower()


class WordCounter(IWordCollectionVisitor):

    def __init__(self, next_visitor: Optional[IWordCollectionVisitor] = None):
        super().__init__(next_visitor)
        self.word_counts = {}

    def visit(self, word: str) -> StrGenerator:
        if word not in self.word_counts:
            self.word_counts[word] = 0
        self.word_counts[word] += 1
        yield word


class Splitter(IWordCollectionVisitor):

    def visit(self, text: str) -> StrGenerator:
        for word_candidate in SPLIT_WORDS_PATTERN.split(text):
            if word_candidate == "" or word_candidate == " ":
                continue
            yield word_candidate


class MyHTMLParser(HTMLParser):
    closest_parent_tag = None
    started = False
    finished = False
    letter_pattern = re.compile(r'\w', re.MULTILINE)

    def __init__(self, visitor: IWordCollectionVisitor, **kwargs):
        super().__init__(**kwargs)
        self._visitor = visitor

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
        text_part = unicodedata.normalize("NFC", data)  # https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
        if self.letter_pattern.search(text_part) is None:
            return
        if self.closest_parent_tag not in {"style", "script", "head", "meta", "title", "html"}:
            print("Encountered some text :", text_part)
            self._visitor.visit_words([text_part])


def count_human_readable_words_in_webpage(url):
    word_counter = WordCounter(WordNormalizer(Splitter()))
    parser = MyHTMLParser(visitor=word_counter)
    with httpx.stream("GET", url) as r:
        for text in r.iter_text():
            parser.feed(text)
            if parser.finished:
                break

    print(f"{repr(word_counter.word_counts)}")
    parser.close()



if __name__ == '__main__':
    count_human_readable_words_in_webpage('https://www.google.pl/')
