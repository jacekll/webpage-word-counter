from count_words import get_words, strip_comments, strip_tags, get_top_n_words


def test_count_words_simple_script():
    with open('../test_simple_utf8.html', 'rb') as f:
        text = f.read().decode("UTF-8")
    result = get_top_n_words(
        get_words(
            strip_tags(
                strip_comments(
                    text
                )
            )
        ),
        1000
    )

    assert {('com', 1),
         ('copy', 1),
         ('dla', 1),
         ('dysk', 1),
         ('firm', 1),
         ('gdzie', 1),
         ('gmail', 1),
         ('google', 2),
         ('grafika', 1),
         ('głosować', 1),
         ('historia', 1),
         ('mapy', 1),
         ('nbsp', 1),
         ('o', 1),
         ('odbędą', 1),
         ('online', 1),
         ('października', 1),
         ('play', 1),
         ('prywatność', 1),
         ('raquo', 1),
         ('reklamuj', 1),
         ('rozwiązania', 1),
         ('się', 3),
         ('sprawdź', 1),
         ('szukaj', 1),
         ('szukanie', 1),
         ('ustawienia', 1),
         ('warunki', 1),
         ('wiadomości', 1),
         ('więcej', 1),
         ('wszystko', 1),
         ('wybory', 1),
         ('youtube', 1),
         ('zaawansowane', 1),
         ('zaloguj', 1)
    } == set(result)
