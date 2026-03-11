from app.adapters.registry import build_adapters


def test_build_default_adapters():
    adapters = build_adapters()
    names = {adapter.source_name for adapter in adapters}
    assert {"mangalib", "mangabuff", "remanga", "senkuro", "dezu", "mangachan"}.issubset(names)


def test_build_selected_adapters():
    adapters = build_adapters(["mangalib", "dezu"])
    names = [adapter.source_name for adapter in adapters]
    assert names == ["mangalib", "dezu"]
