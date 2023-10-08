import sys
from typing import Iterable, Final
from urllib import request

from parse_string import search_for_closing_script_tag


def get_page_content(url: str) -> str:
    with request.urlopen(url) as f:
        return str(f.read())


def count_words(words: Iterable[str]):
    word_counts = {}
    for word in words:
        word_normalized = word.lower()
        word_counts[word_normalized] = word_counts.get(word_normalized, 0) + 1
    return word_counts


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


def strip_comments(html: str):
    current_position = 0
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
    return text[text.find(">") + 1:]


if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    print(
        count_words(
            get_words(
                strip_tags(
                    strip_comments(
                        skip_doctype(f.read())
                    )
                )
            )
        )
    )
    f.close()
