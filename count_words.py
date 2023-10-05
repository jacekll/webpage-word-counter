from urllib import request


def get_page_content(url: str) -> str:
    with request.urlopen(url) as f:
        return str(f.read())


def strip_tags(html: str):
    more_text = True
    end_tag = -1
    while more_text:
        start_tag = html.find("<", end_tag + 1)
        if start_tag == -1:
            yield html[end_tag + 1:]
            break
        yield html[end_tag + 1:start_tag]
        end_tag = html.find(">", start_tag + 1)
        more_text = end_tag != -1


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


if __name__ == "__main__":
    print(get_page_content("https://www.google.pl/"))
