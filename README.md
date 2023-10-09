# Webpage Word Counting

Please see:

1. `count_words_builtin_libs.py` for a program using builtin `html.parser` library.
   This program parses more cases,
   including malformed "<" and ">" characters in inline scripts.
   Apart from standalone usage, it's functions serve as reference for high-level test cases.
2. `count_words.py` for a program not using the builtin `html.parser` library. 
   
   **Limitations:**

   Please see `test_count_words_advanced()` in `tests/test_count_words.py` for details -

   * html entities are not parsed, therefore these are counted as words.
   * malformed "<" and ">" characters in inline scripts are not handled properly, leading to garbled results.
     
Both programs output data in utf-8 and handle any webpage encoding (provided that the encoding is
declared in HTTP response headers of the webpage).

Both programs do not handle client-side generated content.


## Requirements

Python 3.10+, no third-party libraries required.

## Possible next steps

1. Handle authentication and HTTP redirects when fetching the page content
2. Handle content generated with JavaScript
3. Parse HTML entities in `count_words.py`
