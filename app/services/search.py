import re

from rapidfuzz import fuzz
from slugify import slugify

_SPACE_RE = re.compile(r"\s+")


def normalize_title(value: str) -> str:
    normalized = value.lower().replace("ё", "е")
    normalized = re.sub(r"[^\w\s-]", " ", normalized)
    normalized = _SPACE_RE.sub(" ", normalized).strip()
    return normalized


def title_fingerprint(*parts: str) -> str:
    prepared = " ".join(normalize_title(p) for p in parts if p)
    return slugify(prepared)


def fuzzy_score(query: str, candidate: str) -> int:
    return int(fuzz.WRatio(normalize_title(query), normalize_title(candidate)))
