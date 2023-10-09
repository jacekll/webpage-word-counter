from custom_types import TopNWordsResult


def display_and_save_top_results(top_n_words: TopNWordsResult):
    for word, occurences in top_n_words:
        print(f"{word}: {occurences}")
    with open("results.txt", 'w', encoding="UTF-8") as f:
        for word, occurences in top_n_words:
            f.write(f"{word} {occurences}\n")