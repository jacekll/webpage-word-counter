import sys
from collections import Counter
from collections.abc import Generator
from typing import Iterable
from urllib import request

import unicodedata

from parse_string import search_for_closing_script_tag


def get_page_content(url: str) -> str:
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("url should start with http:// or https:// prefix")
    with request.urlopen(url) as response:
        return response.read().decode(response.headers.get_content_charset())


def normalize_word(word: str):
    return word.casefold()


def get_top_n_words(words: Iterable[str], n: int):
    word_counts = Counter()
    word_counts.update(map(normalize_word, words))
    return word_counts.most_common(n)


def get_words(text: Iterable[str]) -> str:
    for text_part in text:
        start_word_index = 0
        length = len(text_part)
        while start_word_index < length:
            while start_word_index < length and not text_part[start_word_index].isalpha():
                start_word_index += 1
            end_word_index = start_word_index
            while end_word_index < length and text_part[end_word_index].isalpha():
                end_word_index += 1
            if end_word_index > start_word_index:
                yield text_part[start_word_index:end_word_index].lower()
            start_word_index = end_word_index


def get_tag_name(tag: str) -> str:
    end_of_name_position = tag.find(" ")
    if end_of_name_position != -1:
        tag = tag[:end_of_name_position]
    else:
        end_of_name_position = tag.find("\n")
        if end_of_name_position != -1:
            tag = tag[:end_of_name_position]
        else:
            end_of_name_position = tag.find("\t")
            if end_of_name_position != -1:
             tag = tag[:end_of_name_position]
    return tag.lower()


def strip_tags(lines: Iterable[str]):
    tag_name = None
    for html in lines:
        more_text = True
        tag_ending_pos = -1
        while more_text:
            if tag_name == 'script':
                start_tag_pos = search_for_closing_script_tag(html, tag_ending_pos + 1)
            else:
                start_tag_pos = html.find("<", tag_ending_pos + 1)
            if tag_name is not None and start_tag_pos == -1:
                yield html[tag_ending_pos + 1:]
                break
            new_tag_ending_pos = html.find(">", start_tag_pos + 1)
            tag = html[start_tag_pos + 1: new_tag_ending_pos].strip()
            tag_name = get_tag_name(tag)
            if tag_name.lstrip("/") not in {"style", "link", "script", "head", "meta", "title"}:
                yield html[tag_ending_pos + 1:start_tag_pos]
                yield " "
            tag_ending_pos = new_tag_ending_pos
            more_text = tag_ending_pos != -1


def strip_comments(html: str) -> Iterable[str]:
    current_position = skip_doctype(html)
    more_text = True
    while more_text:
        start_comment = html.find("<!--", current_position)
        if start_comment == -1:
            yield html[current_position:]
            break
        yield html[current_position:start_comment]
        if start_comment != -1:
            end_comment = html.find("-->", start_comment + 4)
            more_text = end_comment != -1
        current_position = end_comment + 3


def skip_doctype(text: str):
    return text.find(">") + 1 if text.startswith("<doctype") else 0


if __name__ == "__main__":
    text = get_page_content(sys.argv[1])
    print(
        get_top_n_words(
            get_words(
                strip_tags(
                    strip_comments(
                        text
                    )
                )
            )
        )
    )

