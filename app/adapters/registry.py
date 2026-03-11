from collections.abc import Iterable

from app.adapters.base import SourceAdapter
from app.adapters.sources.dezu import DezuAdapter
from app.adapters.sources.mangabuff import MangaBuffAdapter
from app.adapters.sources.mangachan import MangaChanAdapter
from app.adapters.sources.mangalib import MangaLibAdapter
from app.adapters.sources.remanga import ReMangaAdapter
from app.adapters.sources.senkuro import SenkuroAdapter


def build_adapters(enabled: Iterable[str] | None = None) -> list[SourceAdapter]:
    available: dict[str, type[SourceAdapter]] = {
        "mangalib": MangaLibAdapter,
        "mangabuff": MangaBuffAdapter,
        "remanga": ReMangaAdapter,
        "senkuro": SenkuroAdapter,
        "dezu": DezuAdapter,
        "mangachan": MangaChanAdapter,
    }
    if enabled is None:
        return [adapter() for adapter in available.values()]

    selected: list[SourceAdapter] = []
    for name in enabled:
        adapter_cls = available.get(name)
        if adapter_cls:
            selected.append(adapter_cls())
    return selected
