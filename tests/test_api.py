from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_index_disables_stale_browser_cache():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store, max-age=0"
    assert "Medienweite Stichprobe" in response.text
    assert "codingSearch" in response.text
    assert "Kontextlücke" in response.text
    assert "Medienvergleich – Kurzbefund" in response.text
    assert "nicht behandelt / Prüfhinweis" in response.text


def test_dlf_ceuta_report_is_available():
    response = client.get("/berichte/dlf-ceuta")
    assert response.status_code == 200
    assert "Sánchez-freundliche" in response.text
    assert "Auffällige Auslassungen" in response.text
    assert "Tribunal Supremo" in response.text


def test_media_sample_report_is_available():
    response = client.get("/berichte/medienweite-stichprobe")
    assert response.status_code == 200
    assert "314 einzeln begründete Artikelkodierungen" in response.text
    assert "Agenturmeldungen" in response.text


def test_gov_data_report_is_available():
    response = client.get("/berichte/gov-data-abgleich")
    assert response.status_code == 200
    assert "Kriminalität und Staatsangehörigkeit" in response.text
    assert "Marokkaner" in response.text


def test_oerr_schlagseite_report_is_available():
    response = client.get("/berichte/oerr-schlagseite")
    assert response.status_code == 200
    assert "ÖRR-Schlagseite" in response.text
    assert "tagesschau.de" in response.text
    assert "moderat" in response.text


def test_research_api_has_complete_dossier_shape():
    response = client.get("/api/research")
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"media", "articles", "claims", "facts", "omission_examples", "article_codings", "coverage_events", "reach_ranking", "sample_progress", "media_summary", "reliability"}
    rels = {r["medium"]: r for r in data["reliability"]}
    assert {"t-online", "ZDF"} <= set(rels)
    ton = rels["t-online"]
    assert ton["n"] == 21 and ton["direction_robust"] is True
    for rel in rels.values():
        assert 0 <= rel["policy_exact_pct"] <= 100
        assert rel["policy_within1_pct"] >= rel["policy_exact_pct"]
        assert {d["dimension"] for d in rel["per_dimension"]} == {"policy_score", "language_asymmetry", "counterposition", "context_completeness", "omission_risk", "factual_confidence"}
    assert len(data["reach_ranking"]) == 25
    assert [r["rank"] for r in data["reach_ranking"]] == list(range(1, 26))
    assert data["reach_ranking"][0]["label"].startswith("ARD")
    assert all(r["reach_source"].strip() and r["reach_url"].strip() for r in data["reach_ranking"])
    assert all(r["reach_pct"] is None or 0 <= r["reach_pct"] <= 100 for r in data["reach_ranking"])
    assert all({"claim", "status", "topic", "checked_at"} <= set(c) for c in data["claims"])
    assert len(data["article_codings"]) >= 69
    assert all(-2 <= c["policy_score"] <= 2 for c in data["article_codings"])
    assert len({c["url"] for c in data["article_codings"]}) == len(data["article_codings"])
    assert all(c["evidence_note"].strip() for c in data["article_codings"])
    assert len({c["topic"] for c in data["article_codings"]}) >= 4
    assert len(data["coverage_events"]) >= 9
    assert all("T" in event["published_at"] for event in data["coverage_events"])
    assert len(data["sample_progress"]) == len(data["media"])
    assert all(p["fulltext_target"] == 20 and p["topic_target"] == 3 for p in data["sample_progress"])
    assert all(p["mature"] == (p["editorial_fulltexts"] >= 20 and p["topic_count"] >= 3) for p in data["sample_progress"])
    assert len(data["media_summary"]) == len(data["media"])
    assert all(0 <= s["omission_rate"] <= 1 for s in data["media_summary"] if s["omission_rate"] is not None)
    assert all("Agentur" not in topic for p in data["sample_progress"] for topic in p["fulltext_topics"])
    dlf = next(p for p in data["sample_progress"] if p["medium"] == "Deutschlandfunk")
    assert dlf["mature"] is True
    assert dlf["editorial_fulltexts"] == 20
    assert dlf["topic_count"] >= 9
    taz = next(p for p in data["sample_progress"] if p["medium"] == "taz")
    assert taz["mature"] is True
    assert taz["editorial_fulltexts"] == 20
    assert taz["topic_count"] >= 5
    nius = next(p for p in data["sample_progress"] if p["medium"] == "NIUS")
    assert nius["mature"] is True
    assert nius["editorial_fulltexts"] == 20
    assert nius["topic_count"] >= 9
    berlin = next(p for p in data["sample_progress"] if p["medium"] == "Berliner Zeitung")
    assert berlin["mature"] is True
    assert berlin["editorial_fulltexts"] == 20
    assert berlin["topic_count"] >= 6
    focus = next(p for p in data["sample_progress"] if p["medium"] == "FOCUS")
    assert focus["mature"] is True
    assert focus["editorial_fulltexts"] >= 20
    assert focus["topic_count"] >= 7
    tagesspiegel = next(p for p in data["sample_progress"] if p["medium"] == "Tagesspiegel")
    assert tagesspiegel["mature"] is True
    assert tagesspiegel["editorial_fulltexts"] == 20
    assert tagesspiegel["topic_count"] >= 5


def test_research_csv_exports_article_level_codings():
    response = client.get("/api/research.csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "medium,title,url,topic" in response.text
    assert "language_asymmetry" in response.text
    assert ",2,1,0,2,1,Volltext," in response.text
    assert "Deutschlandfunk" in response.text
