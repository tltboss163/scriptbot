from app.adapters.http_adapter import GenericHtmlAdapter


class MangaLibAdapter(GenericHtmlAdapter):
    source_name = "mangalib"
    base_url = "https://mangalib.me"
    search_path = "/ru/search?title={query}"
    search_item_selector = "a.media-card"
    search_title_selector = ".media-card__name"
    manga_title_selector = "h1"
    manga_description_selector = ".media-description__text"
    manga_cover_selector = "img.media-sidebar__cover"
    chapter_item_selector = "a.chapter-item"
