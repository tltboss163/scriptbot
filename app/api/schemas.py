from pydantic import BaseModel


class SourceCandidateOut(BaseModel):
    source: str
    source_id: str
    title: str
    aliases: list[str]
    url: str
    chapter_count: int
    cover_url: str | None


class AggregatedResultOut(BaseModel):
    canonical_title: str
    fingerprint: str
    best_source: str
    total_sources: int
    best_chapter_count: int
    candidates: list[SourceCandidateOut]


class MangaCardOut(BaseModel):
    source: str
    source_id: str
    title: str
    title_original: str | None
    aliases: list[str]
    description: str | None
    genres: list[str]
    status: str | None
    cover_url: str | None
    chapter_count: int
    url: str | None


class ChapterOut(BaseModel):
    source: str
    manga_id: str
    chapter_id: str
    number: str
    title: str | None
    pages: int | None
