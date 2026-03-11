from abc import ABC, abstractmethod

from app.models.manga import Chapter, MangaCard, SourceSearchResult


class SourceAdapter(ABC):
    source_name: str

    @abstractmethod
    async def search(self, query: str) -> list[SourceSearchResult]:
        """Search manga inside source."""

    @abstractmethod
    async def get_manga(self, source_id: str) -> MangaCard:
        """Get full manga metadata."""

    @abstractmethod
    async def get_chapters(self, source_id: str) -> list[Chapter]:
        """Get chapter list ordered ASC."""

    @abstractmethod
    async def get_pages(self, chapter_id: str) -> list[str]:
        """Get full list of image URLs for chapter."""
