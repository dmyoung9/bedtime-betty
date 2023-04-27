import re

import tiktoken

from .config import MODEL

NUMBERED_LINE_REGEX = r"^(?:[\d\s\W]+)?(.*)$"
TITLE_LINE_REGEX = r"^(?:[\d\s\W]+)(.*)$"


def count_tokens(text, model=MODEL):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def clean_numbered_content(content):
    clean_lines = []
    for line in content.splitlines():
        clean_line = re.match(NUMBERED_LINE_REGEX, line.rstrip()).groups()[0]
        clean_line = clean_line.rstrip(".").lower()
        clean_lines.append(clean_line)

    return clean_lines
