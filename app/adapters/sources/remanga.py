from app.adapters.http_adapter import GenericHtmlAdapter


class ReMangaAdapter(GenericHtmlAdapter):
    source_name = "remanga"
    base_url = "https://remanga.org"
    search_path = "/search?query={query}"
    search_item_selector = "a.card"
    search_title_selector = ".card__title"
    chapter_item_selector = "a.chapter-item"
