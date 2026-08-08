from app.analyzer import analyze_local
from app.db import initialize, rows


def test_finds_loaded_term_with_quote():
    text = ("Die sogenannte Abschottung der Europäischen Union sei umstritten. "
            "Das ist ein ausreichend langer Beispieltext für die Analyse des Artikels.")
    result = analyze_local(text)
    terms = {item["term"] for item in result["findings"]}
    assert "abschottung" in terms
    assert "umstritten" in terms
    assert all(item["quote"] for item in result["findings"])


def test_neutral_text_does_not_invent_orientation():
    text = "Der Bericht nennt eine Quelle. Eine zweite Quelle widerspricht der ersten Darstellung."
    result = analyze_local(text)
    assert "orientation" not in result
    assert result["signal_count"] == 0


def test_research_database_is_seeded():
    initialize()
    assert len(rows("media")) >= 12
    assert any(x["medium"] == "Deutschlandfunk" for x in rows("articles"))
    assert any("offen" in x["status"] for x in rows("claims"))
    assert len(rows("facts")) >= 4
    assert len(rows("omission_examples")) >= 4


def test_initialize_is_idempotent():
    initialize()
    before = [(x["id"], x["name"]) for x in rows("media")]
    article_count = len(rows("articles"))
    initialize()
    assert [(x["id"], x["name"]) for x in rows("media")] == before
    assert len(rows("articles")) == article_count
    assert all(x["topic"] != "Allgemein" for x in rows("claims"))
