def convert_leading_spaces_to_tabs(line: str, tab_width: int = 4) -> str:
    leading_spaces = len(line) - len(line.lstrip(' '))
    tabs = '\t' * (leading_spaces // tab_width)
    return tabs + line.lstrip(' ')