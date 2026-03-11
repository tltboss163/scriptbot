from app.adapters.http_adapter import GenericHtmlAdapter


class MangaBuffAdapter(GenericHtmlAdapter):
    source_name = "mangabuff"
    base_url = "https://mangabuff.ru"
    search_path = "/search?q={query}"
    search_item_selector = "a.manga-card"
    search_title_selector = ".manga-card__title"
    chapter_item_selector = "a.chapter"
