import re

from rapidfuzz import fuzz
from slugify import slugify

_SPACE_RE = re.compile(r"\s+")
_RU_EN = str.maketrans(
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ы": "y",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
)


def normalize_title(value: str) -> str:
    normalized = value.lower().replace("ё", "е")
    normalized = re.sub(r"[^\w\s-]", " ", normalized)
    normalized = _SPACE_RE.sub(" ", normalized).strip()
    return normalized


def translit_ru_to_en(value: str) -> str:
    normalized = normalize_title(value)
    return normalized.translate(_RU_EN)


def title_fingerprint(*parts: str) -> str:
    prepared = " ".join(normalize_title(p) for p in parts if p)
    return slugify(prepared)


def fuzzy_score(query: str, candidate: str) -> int:
    q = normalize_title(query)
    c = normalize_title(candidate)
    direct = fuzz.WRatio(q, c)
    translit = fuzz.WRatio(translit_ru_to_en(q), translit_ru_to_en(c))
    return int(max(direct, translit))
