from typing import List, Union, Iterable


def trim(s: Iterable):
    if isinstance(s, str):
        return s.strip()
    elif isinstance(s, list):
        return [x for x in s if x]
    elif isinstance(s, tuple):
        return tuple([x for x in s if x])
    elif isinstance(s, set):
        return set([x for x in s if x])
    else:
        return ""


def condense_ws(s: str):
        _s = s.replace("\t", " ")\
            .replace("\n", " ")\
            .replace("\r", " ")

        return " ".join(trim(_s.split(" ")))