from app.adapters.http_adapter import GenericHtmlAdapter


class SenkuroAdapter(GenericHtmlAdapter):
    source_name = "senkuro"
    base_url = "https://senkuro.com"
    search_path = "/search/{query}"
    search_item_selector = "a.title-card"
    search_title_selector = ".title-card__name"
    chapter_item_selector = "a.chapter-link"
