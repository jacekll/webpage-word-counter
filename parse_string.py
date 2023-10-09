from collections import deque
from typing import Final, Any, Optional


class Stack:
    def __init__(self):
        self.data = deque()

    def push(self, item: Any) -> None:
        return self.data.append(item)

    def pop(self) -> Any:
        return self.data.pop()

    def peek(self) -> Optional[Any]:
        return self.data[-1] if self.data else None

    def is_empty(self) -> bool:
        return not self.data


def search_for_closing_script_tag(text: str, start_index: int) -> int:
    """Returns the position of closing </script> or -1 if it was not found."""
    QUOTE_CHARS: Final[set[str]] = {'"', "'"}
    ESCAPE_CHAR: Final[str] = '\\'
    open_quotes = Stack()
    escape_count = 0
    text_length = len(text)
    for idx in range(start_index, text_length):
        char = text[idx]
        if char == ESCAPE_CHAR:
            escape_count = (escape_count + 1) % 2
        else:
            if char in QUOTE_CHARS and escape_count == 0:
                if open_quotes.peek() == char:
                    open_quotes.pop()
                else:
                    open_quotes.push(char)
            else:
                # todo better string search algorithm:
                if open_quotes.is_empty() and text[idx:idx + 9].lower() == "</script>":
                    return idx
    return -1
