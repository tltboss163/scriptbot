import asyncio
import json
from dataclasses import asdict

from app.adapters.base import SourceAdapter
from app.models.manga import Chapter, MangaCard, SourceSearchResult
from app.services.aggregator import SearchAggregator


class FakeAdapter(SourceAdapter):
    def __init__(self, source_name: str, results: list[SourceSearchResult]) -> None:
        self.source_name = source_name
        self._results = results

    async def search(self, query: str) -> list[SourceSearchResult]:
        return [item for item in self._results if query.lower() in item.title.lower()]

    async def get_manga(self, source_id: str) -> MangaCard:
        return MangaCard(source=self.source_name, source_id=source_id, title=source_id)

    async def get_chapters(self, source_id: str) -> list[Chapter]:
        return []

    async def get_pages(self, chapter_id: str) -> list[str]:
        return []


async def main() -> None:
    adapters: list[SourceAdapter] = [
        FakeAdapter(
            "mangalib",
            [
                SourceSearchResult("mangalib", "naruto", "Naruto", ["Наруто"], "https://mangalib.me/naruto", 700),
                SourceSearchResult("mangalib", "bleach", "Bleach", [], "https://mangalib.me/bleach", 686),
            ],
        ),
        FakeAdapter(
            "mangachan",
            [
                SourceSearchResult("mangachan", "naruto-ru", "Наруто", ["Naruto"], "https://mangachan.me/naruto", 650),
            ],
        ),
        FakeAdapter(
            "remanga",
            [
                SourceSearchResult("remanga", "naruto-shippuuden", "Naruto Shippuuden", ["Наруто Шипуден"], "https://remanga.org/naruto", 500),
            ],
        ),
    ]

    result = await SearchAggregator(adapters).search("naruto")
    print(json.dumps([asdict(item) for item in result], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
