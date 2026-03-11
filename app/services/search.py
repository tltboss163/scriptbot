import re
from difflib import SequenceMatcher

_SPACE_RE = re.compile(r"\s+")
_NON_WORD_RE = re.compile(r"[^\w\s-]")

_RU_EN_MAP = {
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


def normalize_title(value: str) -> str:
    normalized = value.lower().replace("ё", "е")
    normalized = _NON_WORD_RE.sub(" ", normalized)
    normalized = _SPACE_RE.sub(" ", normalized).strip()
    return normalized


def translit_ru_to_en(value: str) -> str:
    normalized = normalize_title(value)
    return "".join(_RU_EN_MAP.get(ch, ch) for ch in normalized)


def _simple_slug(value: str) -> str:
    value = normalize_title(value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def title_fingerprint(*parts: str) -> str:
    prepared = " ".join(normalize_title(part) for part in parts if part)
    return _simple_slug(prepared)


def _ratio(a: str, b: str) -> int:
    return int(100 * SequenceMatcher(None, a, b).ratio())


def fuzzy_score(query: str, candidate: str) -> int:
    q = normalize_title(query)
    c = normalize_title(candidate)
    direct = _ratio(q, c)
    translit = _ratio(translit_ru_to_en(q), translit_ru_to_en(c))
    return max(direct, translit)
