from __future__ import annotations

import asyncio
from collections import defaultdict

from app.adapters.base import SourceAdapter
from app.models.manga import AggregatedResult, SourceSearchResult
from app.services.search import fuzzy_score, title_fingerprint


class SearchAggregator:
    def __init__(self, adapters: list[SourceAdapter]) -> None:
        self.adapters = adapters

    async def search(self, query: str) -> list[AggregatedResult]:
        tasks = [adapter.search(query) for adapter in self.adapters]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        grouped: dict[str, list[SourceSearchResult]] = defaultdict(list)
        for payload in raw_results:
            if isinstance(payload, Exception):
                continue
            for item in payload:
                fp = title_fingerprint(item.title, *item.aliases)
                grouped[fp].append(item)

        aggregated: list[AggregatedResult] = []
        for fp, candidates in grouped.items():
            best = max(candidates, key=lambda x: x.chapter_count)
            canonical = best.title
            aggregated.append(
                AggregatedResult(
                    canonical_title=canonical,
                    fingerprint=fp,
                    best_source=best.source,
                    total_sources=len(candidates),
                    best_chapter_count=best.chapter_count,
                    candidates=sorted(candidates, key=lambda x: x.chapter_count, reverse=True),
                )
            )

        aggregated.sort(
            key=lambda item: (
                fuzzy_score(query, item.canonical_title),
                item.best_chapter_count,
                -item.total_sources,
            ),
            reverse=True,
        )
        return aggregated
