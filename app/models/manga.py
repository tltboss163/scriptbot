from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class MangaCard:
    source: str
    source_id: str
    title: str
    title_original: str | None = None
    aliases: list[str] = field(default_factory=list)
    description: str | None = None
    genres: list[str] = field(default_factory=list)
    status: str | None = None
    cover_url: str | None = None
    chapter_count: int = 0
    last_updated: datetime | None = None
    url: str | None = None


@dataclass(slots=True)
class Chapter:
    source: str
    manga_id: str
    chapter_id: str
    number: str
    title: str | None
    pages: int | None = None


@dataclass(slots=True)
class SourceSearchResult:
    source: str
    source_id: str
    title: str
    aliases: list[str]
    url: str
    chapter_count: int = 0
    cover_url: str | None = None


@dataclass(slots=True)
class AggregatedResult:
    canonical_title: str
    fingerprint: str
    best_source: str
    total_sources: int
    best_chapter_count: int
    candidates: list[SourceSearchResult]
