from urllib import request

from custom_types import TopNWordsResult


def display_and_save_top_results(top_n_words: TopNWordsResult):
    for word, occurences in top_n_words:
        print(f"{word}: {occurences}")
    with open("results.txt", 'w', encoding="UTF-8") as f:
        for word, occurences in top_n_words:
            f.write(f"{word} {occurences}\n")


def get_page_content(url: str) -> str:
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("url should start with http:// or https:// prefix")
    with request.urlopen(url) as response:
        return response.read().decode(response.headers.get_content_charset())
