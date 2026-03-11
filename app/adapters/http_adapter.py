from __future__ import annotations

from urllib.parse import quote, urljoin

import httpx
from bs4 import BeautifulSoup

from app.adapters.base import SourceAdapter
from app.models.manga import Chapter, MangaCard, SourceSearchResult


class GenericHtmlAdapter(SourceAdapter):
    source_name = "generic"
    base_url: str = ""
    search_path: str = "/search?query={query}"

    # selectors
    search_item_selector = "a"
    search_title_selector = None
    search_link_attr = "href"

    manga_title_selector = "h1"
    manga_description_selector = "meta[name='description']"
    manga_cover_selector = "img"

    chapter_item_selector = "a"

    def __init__(self, timeout: float = 20.0) -> None:
        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": "ScriptBot/1.0 (+https://scriptbot.local)"},
        )

    async def _fetch_html(self, path: str) -> BeautifulSoup:
        url = path if path.startswith("http") else urljoin(self.base_url, path)
        response = await self._client.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    async def search(self, query: str) -> list[SourceSearchResult]:
        path = self.search_path.format(query=quote(query))
        soup = await self._fetch_html(path)
        results: list[SourceSearchResult] = []
        for item in soup.select(self.search_item_selector)[:20]:
            href = item.get(self.search_link_attr)
            if not href:
                continue
            title_node = item.select_one(self.search_title_selector) if self.search_title_selector else item
            title = title_node.get_text(" ", strip=True) if title_node else ""
            if not title:
                continue
            source_id = href.rstrip("/").split("/")[-1]
            results.append(
                SourceSearchResult(
                    source=self.source_name,
                    source_id=source_id,
                    title=title,
                    aliases=[],
                    url=urljoin(self.base_url, href),
                )
            )
        return results

    async def get_manga(self, source_id: str) -> MangaCard:
        soup = await self._fetch_html(f"/manga/{source_id}")
        title_node = soup.select_one(self.manga_title_selector)
        title = title_node.get_text(" ", strip=True) if title_node else source_id
        description = None
        desc_node = soup.select_one(self.manga_description_selector)
        if desc_node:
            description = (desc_node.get("content") or desc_node.get_text(" ", strip=True)).strip()
        cover = None
        cover_node = soup.select_one(self.manga_cover_selector)
        if cover_node:
            cover = cover_node.get("src")
            if cover:
                cover = urljoin(self.base_url, cover)

        chapters = await self.get_chapters(source_id)
        return MangaCard(
            source=self.source_name,
            source_id=source_id,
            title=title,
            description=description,
            cover_url=cover,
            chapter_count=len(chapters),
            url=urljoin(self.base_url, f"/manga/{source_id}"),
        )

    async def get_chapters(self, source_id: str) -> list[Chapter]:
        soup = await self._fetch_html(f"/manga/{source_id}")
        items = soup.select(self.chapter_item_selector)
        chapters: list[Chapter] = []
        for item in items:
            href = item.get("href")
            if not href or "chapter" not in href:
                continue
            chapter_id = href.rstrip("/").split("/")[-1]
            title = item.get_text(" ", strip=True)
            number = chapter_id
            chapters.append(
                Chapter(
                    source=self.source_name,
                    manga_id=source_id,
                    chapter_id=chapter_id,
                    number=number,
                    title=title,
                )
            )
        return chapters

    async def get_pages(self, chapter_id: str) -> list[str]:
        soup = await self._fetch_html(f"/chapter/{chapter_id}")
        pages: list[str] = []
        for img in soup.select("img"):
            src = img.get("src")
            if not src:
                continue
            lower = src.lower()
            if any(lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                pages.append(urljoin(self.base_url, src))
        return pages

    async def close(self) -> None:
        await self._client.aclose()
