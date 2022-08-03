from typing import List, Union, Iterable
import unicodedata


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
    _s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ")

    return " ".join(trim(_s.split(" ")))


def after(substr: str, s: str):
    ...


def before(substr: str, s: str):
    ...


def convert_unicode(s: str):
    return unicodedata.normalize("NFKD", s).encode("utf-8", "ignore").decode("utf-8")


print(convert_unicode("This is \u00bd"))
