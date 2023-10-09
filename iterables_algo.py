from copy import copy

from iterables import ChunkedIterable, ChunkedIterator


def find_first_pattern_index(text: ChunkedIterator, pattern: str):
    lookup_text: ChunkedIterator = copy(text)
    found = 0
    pattern_len = len(pattern)
    for i, c in enumerate(lookup_text):
        if c == pattern[found]:
            if found == pattern_len - 1:
                return i - pattern_len + 1
            found += 1
        else:
            found = 0
    return -1


def strip_comments(html: str) -> ChunkedIterable:
    it = ChunkedIterable(html)
    end_comment = 0
    more_text = html != ""
    while more_text:
        start_comment = html.find("<!--", end_comment)
        if start_comment == -1:
            it.add_chunk(end_comment, len(html))
            break
        else:
            if start_comment > end_comment:
                it.add_chunk(end_comment, start_comment - 1)
            end_comment = html.find("-->", start_comment + 4, ) + 3
    return it