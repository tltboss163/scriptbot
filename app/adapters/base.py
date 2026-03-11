from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MangaRef:
    source: str
    source_id: str
    title: str
    aliases: list[str]
    url: str


class SourceAdapter(ABC):
    source_name: str

    @abstractmethod
    async def search(self, query: str) -> list[MangaRef]:
        """Search manga by query inside source."""

    @abstractmethod
    async def get_manga(self, source_id: str) -> dict:
        """Get manga card metadata."""

    @abstractmethod
    async def get_chapters(self, source_id: str) -> list[dict]:
        """Return chapter list with numbers and dates."""

    @abstractmethod
    async def get_pages(self, chapter_id: str) -> list[str]:
        """Return image page URLs in strict order."""
