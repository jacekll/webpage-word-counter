from typing import Final

import pytest

from string_functions import search_for_closing_script_tag

COMMON_CASES: Final = [
        (""" \\'</script>' </script>""", 3),
        ("", -1),
        (" ", -1),
        (" </script>", 1),
        (" '</script>' ", -1),
        (" '</script>' </script>", 13),
        (' "</script>" </script>', 13),
    ]

@pytest.mark.parametrize(
    "text, expected_index", [
        ("</script>", 0),

    ] + COMMON_CASES
)
def test_search_for_closing_script_tag(text, expected_index):
    assert search_for_closing_script_tag(text, 0) == expected_index


@pytest.mark.parametrize(
    "text, expected_index",[
        ("</script>", -1),
    ] + COMMON_CASES
)
def test_search_for_closing_script_tag_with_non_zero_starting_index(text, expected_index):
    assert search_for_closing_script_tag(text, 1) == expected_index