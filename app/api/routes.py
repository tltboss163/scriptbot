from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Query

from app.adapters.registry import build_adapters
from app.config import settings
from app.api.schemas import AggregatedResultOut, ChapterOut, MangaCardOut
from app.services.aggregator import SearchAggregator

router = APIRouter(prefix="/api", tags=["api"])
adapters = build_adapters(settings.enabled_sources)
adapter_map = {adapter.source_name: adapter for adapter in adapters}
aggregator = SearchAggregator(adapters)


@router.get("/sources")
async def list_sources() -> dict[str, list[str]]:
    return {"sources": sorted(adapter_map)}


@router.get("/search", response_model=list[AggregatedResultOut])
async def search(q: str = Query(min_length=2)) -> list[AggregatedResultOut]:
    data = await aggregator.search(q)
    return [AggregatedResultOut.model_validate(asdict(item)) for item in data]


@router.get("/manga/{source}/{source_id}", response_model=MangaCardOut)
async def manga_card(source: str, source_id: str) -> MangaCardOut:
    adapter = adapter_map.get(source)
    if not adapter:
        raise HTTPException(status_code=404, detail="Source not found")
    card = await adapter.get_manga(source_id)
    return MangaCardOut.model_validate(asdict(card))


@router.get("/manga/{source}/{source_id}/chapters", response_model=list[ChapterOut])
async def manga_chapters(source: str, source_id: str) -> list[ChapterOut]:
    adapter = adapter_map.get(source)
    if not adapter:
        raise HTTPException(status_code=404, detail="Source not found")
    chapters = await adapter.get_chapters(source_id)
    return [ChapterOut.model_validate(asdict(item)) for item in chapters]
