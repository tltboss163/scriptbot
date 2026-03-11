from app.adapters.http_adapter import GenericHtmlAdapter


class MangaChanAdapter(GenericHtmlAdapter):
    source_name = "mangachan"
    base_url = "https://mangachan.me"
    search_path = "/search?title={query}"
    search_item_selector = "a.content_row"
    search_title_selector = "b"
    chapter_item_selector = "a.chapter-link"
