from app.services.search import fuzzy_score, normalize_title, title_fingerprint, translit_ru_to_en


def test_normalize_title():
    assert normalize_title(" Ёкай!!!   test ") == "екай test"


def test_translit_not_empty():
    assert translit_ru_to_en("наруто")


def test_title_fingerprint_stable():
    assert title_fingerprint("Наруто", "Naruto") == title_fingerprint(" naruto ", "Наруто")


def test_fuzzy_score_positive():
    assert fuzzy_score("naruto", "naruto shippuden") > 0
