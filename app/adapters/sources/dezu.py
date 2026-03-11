from app.adapters.http_adapter import GenericHtmlAdapter


class DezuAdapter(GenericHtmlAdapter):
    source_name = "dezu"
    base_url = "https://dezu.ru"
    search_path = "/search?query={query}"
    search_item_selector = "a.result-item"
    search_title_selector = ".result-item__title"
    chapter_item_selector = "a.chapter-item"
