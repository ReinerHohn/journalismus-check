from __future__ import annotations

import csv
import io
from html import escape
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

from .analyzer import analyze_local
from .db import initialize, rows
from .goal_config import OERR_ONLINE, TARGET_ARTICLES, TOP30
from .llm import analyze_with_model
from .reliability_data import CODER2_BY_MEDIUM, CODER2_LABEL, CODER2_SCALE


DIMENSIONS = ("policy_score", "language_asymmetry", "counterposition",
              "context_completeness", "omission_risk", "factual_confidence")


def _weighted_kappa(pairs: list[tuple[int, int]], lo: int, hi: int) -> float | None:
    """Linear-weighted Cohen's kappa for an ordinal scale lo..hi."""
    categories = list(range(lo, hi + 1))
    n = len(pairs)
    if n == 0:
        return None
    span = (hi - lo) or 1
    weight = lambda a, b: 1 - abs(a - b) / span
    row = {c: sum(1 for a, _ in pairs if a == c) / n for c in categories}
    col = {c: sum(1 for _, b in pairs if b == c) / n for c in categories}
    observed = sum(weight(a, b) for a, b in pairs) / n
    expected = sum(weight(a, b) * row[a] * col[b] for a in categories for b in categories)
    if expected >= 1:
        return 1.0
    return round((observed - expected) / (1 - expected), 3)


def reliability_report(codings: list[dict]) -> list[dict]:
    """Compare the first coding with the blind second coding, one entry per medium."""
    reports = [_reliability_one(medium, coder2, codings)
               for medium, coder2 in CODER2_BY_MEDIUM.items()]
    return [report for report in reports if report["n"] > 0]


def _reliability_one(medium: str, coder2: dict, codings: list[dict]) -> dict:
    by_url = {row["url"]: row for row in codings if row["medium"] == medium}
    matched = [(by_url[url], second) for url, second in coder2.items() if url in by_url]
    n = len(matched)
    if not n:
        return {"medium": medium, "n": 0}

    def pairs(index: int) -> list[tuple[int, int]]:
        key = DIMENSIONS[index]
        return [(int(first[key]), int(second[index])) for first, second in matched]

    policy = pairs(0)
    diffs = [a - b for a, b in policy]
    per_dimension = []
    for i, key in enumerate(DIMENSIONS):
        p = pairs(i)
        exact = sum(1 for a, b in p if a == b) / n
        within1 = sum(1 for a, b in p if abs(a - b) <= 1) / n
        per_dimension.append({
            "dimension": key,
            "exact_pct": round(exact * 100, 1),
            "within1_pct": round(within1 * 100, 1),
            "weighted_kappa": _weighted_kappa(p, 0 if i else -2, 2),
        })

    coder1_mean = round(sum(a for a, _ in policy) / n, 3)
    coder2_mean = round(sum(b for _, b in policy) / n, 3)
    return {
        "medium": medium,
        "label": CODER2_LABEL,
        "scale": CODER2_SCALE,
        "n": n,
        "policy_exact_pct": round(sum(1 for d in diffs if d == 0) / n * 100, 1),
        "policy_within1_pct": round(sum(1 for d in diffs if abs(d) <= 1) / n * 100, 1),
        "policy_mean_abs_diff": round(sum(abs(d) for d in diffs) / n, 3),
        "policy_weighted_kappa": _weighted_kappa(policy, -2, 2),
        "coder1_policy_mean": coder1_mean,
        "coder2_policy_mean": coder2_mean,
        "direction_robust": (coder1_mean < -0.2 and coder2_mean < -0.2)
                            or (coder1_mean > 0.2 and coder2_mean > 0.2),
        "per_dimension": per_dimension,
    }


app = FastAPI(title="Journalismus-Check", version="0.1.0")
INDEX = Path(__file__).with_name("static").joinpath("index.html")
DLF_CEUTA_REPORT = Path(__file__).parent.parent.joinpath("reports", "dlf-ceuta-analyse.md")
MEDIA_SAMPLE_REPORT = Path(__file__).parent.parent.joinpath("reports", "medienweite-stichprobe-stand-2026-08-08.md")
GOV_DATA_REPORT = Path(__file__).parent.parent.joinpath("reports", "gov-data-abgleich-2026-08-08.md")
OERR_SCHLAGSEITE_REPORT = Path(__file__).parent.parent.joinpath("reports", "oerr-schlagseite-2026-08-08.md")
OERR_BEVOELKERUNG_REPORT = Path(__file__).parent.parent.joinpath("reports", "oerr-vs-bevoelkerung-2026-08-08.md")
OERR_BEITRAGSZAHLER_REPORT = Path(__file__).parent.parent.joinpath("reports", "oerr-beitragszahler-abgleich-2026-08-08.md")
initialize()

SAMPLE_TARGET_FULLTEXTS = 20
SAMPLE_TARGET_TOPICS = 3


def sample_progress(media: list[dict], codings: list[dict]) -> list[dict]:
    """Return the auditable maturity gate used by the dashboard.

    Agency copy is retained in the corpus but cannot satisfy the editorial-text
    threshold. Likewise, partial text, metadata and paywalled excerpts are not
    counted as checked full texts.
    """
    result = []
    for outlet in media:
        outlet_codings = [row for row in codings if row["medium"] == outlet["name"]]
        editorial = [row for row in outlet_codings if "agentur" not in row["genre"].lower()]
        fulltexts = [row for row in editorial if row["access_level"].lower() == "volltext"]
        topics = sorted({row["topic"] for row in fulltexts})
        result.append({
            "medium": outlet["name"],
            "coded_total": len(outlet_codings),
            "editorial_total": len(editorial),
            "editorial_fulltexts": len(fulltexts),
            "fulltext_target": SAMPLE_TARGET_FULLTEXTS,
            "fulltext_remaining": max(0, SAMPLE_TARGET_FULLTEXTS - len(fulltexts)),
            "fulltext_topics": topics,
            "topic_count": len(topics),
            "topic_target": SAMPLE_TARGET_TOPICS,
            "topic_remaining": max(0, SAMPLE_TARGET_TOPICS - len(topics)),
            "mature": len(fulltexts) >= SAMPLE_TARGET_FULLTEXTS and len(topics) >= SAMPLE_TARGET_TOPICS,
        })
    return sorted(result, key=lambda row: (row["mature"], row["editorial_fulltexts"], row["topic_count"], row["medium"]))


def media_summary(media: list[dict], codings: list[dict]) -> list[dict]:
    """Aggregate article-level scores without turning omission risk into intent."""
    result = []
    for outlet in media:
        rows_for_medium = [row for row in codings if row["medium"] == outlet["name"]]
        fulltexts = [row for row in rows_for_medium
                     if "agentur" not in row["genre"].lower()
                     and row["access_level"].lower() == "volltext"]
        omission = [row for row in fulltexts if row["omission_risk"] >= 1]
        high_omission = [row for row in fulltexts if row["omission_risk"] >= 2]
        result.append({
            "medium": outlet["name"],
            "profile": outlet["profile"],
            "editorial_fulltexts": len(fulltexts),
            "topic_count": len({row["topic"] for row in fulltexts}),
            "policy_mean": round(sum(row["policy_score"] for row in fulltexts) / len(fulltexts), 3) if fulltexts else None,
            "omission_count": len(omission),
            "omission_rate": round(len(omission) / len(fulltexts), 3) if fulltexts else None,
            "high_omission_count": len(high_omission),
            "mature": len(fulltexts) >= SAMPLE_TARGET_FULLTEXTS and len({row["topic"] for row in fulltexts}) >= SAMPLE_TARGET_TOPICS,
        })
    return sorted(result, key=lambda row: (row["mature"], row["medium"]))


def goal_progress(codings: list[dict]) -> dict:
    """Auditierbarer Stand gegenüber dem Forschungsziel.

    Gezählt wird jeder nach Migrationshaltung analysierte Artikel eines Mediums
    (``analyzed`` = alle Kodierungen). Zusätzlich wird ``editorial_fulltexts``
    ausgewiesen, weil ein Richtungsbefund laut METHODE.md nur auf redaktionellen
    Volltexten beruht. Ein Medium gilt für das Ziel als erfüllt, sobald es die
    jeweilige Zielzahl analysierter Artikel erreicht.
    """
    def counts(name: str) -> tuple[int, int]:
        rows_for = [row for row in codings if row["medium"] == name]
        fulltexts = [row for row in rows_for
                     if "agentur" not in row["genre"].lower()
                     and row["access_level"].lower() == "volltext"]
        return len(rows_for), len(fulltexts)

    top30 = []
    for outlet in TOP30:
        analyzed, fulltexts = counts(outlet["name"])
        top30.append({
            "rank": outlet["rank"], "medium": outlet["name"], "brand": outlet["brand"],
            "kind": outlet["kind"], "analyzed": analyzed, "editorial_fulltexts": fulltexts,
            "target": TARGET_ARTICLES, "remaining": max(0, TARGET_ARTICLES - analyzed),
            "met": analyzed >= TARGET_ARTICLES,
        })

    oerr = []
    for outlet in OERR_ONLINE:
        analyzed, fulltexts = counts(outlet["name"])
        target = outlet["min_articles"]
        oerr.append({
            "medium": outlet["name"], "brand": outlet["brand"], "analyzed": analyzed,
            "editorial_fulltexts": fulltexts, "target": target,
            "remaining": max(0, target - analyzed),
            "covered": analyzed > 0, "met": analyzed >= target,
        })

    return {
        "target_articles": TARGET_ARTICLES,
        "top30": top30,
        "top30_met": sum(1 for row in top30 if row["met"]),
        "top30_total": len(top30),
        "oerr_online": oerr,
        "oerr_covered": sum(1 for row in oerr if row["covered"]),
        "oerr_met": sum(1 for row in oerr if row["met"]),
        "oerr_total": len(oerr),
        "goal_complete": all(row["met"] for row in top30) and all(row["met"] for row in oerr),
    }


class AnalysisRequest(BaseModel):
    text: str = Field(min_length=80, max_length=100_000)
    deep: bool = False


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(
        INDEX.read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.get("/berichte/dlf-ceuta", response_class=HTMLResponse)
def dlf_ceuta_report() -> HTMLResponse:
    report = escape(DLF_CEUTA_REPORT.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"""<!doctype html><html lang=\"de\"><meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
        <title>DLF-Ceuta-Mediencheck</title>
        <style>body{{max-width:920px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui;color:#18211b;background:#f5f3ec}}
        pre{{white-space:pre-wrap;font:inherit;background:white;padding:1.5rem;border-radius:12px}}a{{color:#075c45}}</style>
        <p><a href=\"/\">← Dashboard</a></p><pre>{report}</pre></html>""",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.get("/berichte/medienweite-stichprobe", response_class=HTMLResponse)
def media_sample_report() -> HTMLResponse:
    report = escape(MEDIA_SAMPLE_REPORT.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"""<!doctype html><html lang=\"de\"><meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
        <title>Medienweite Migrationsstichprobe</title>
        <style>body{{max-width:920px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui;color:#18211b;background:#f5f3ec}}
        pre{{white-space:pre-wrap;font:inherit;background:white;padding:1.5rem;border-radius:12px}}a{{color:#075c45}}</style>
        <p><a href=\"/\">← Dashboard</a></p><pre>{report}</pre></html>""",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.get("/berichte/gov-data-abgleich", response_class=HTMLResponse)
def gov_data_report() -> HTMLResponse:
    report = escape(GOV_DATA_REPORT.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"""<!doctype html><html lang=\"de\"><meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
        <title>gov-data-Abgleich</title>
        <style>body{{max-width:920px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui;color:#18211b;background:#f5f3ec}}
        pre{{white-space:pre-wrap;font:inherit;background:white;padding:1.5rem;border-radius:12px}}a{{color:#075c45}}</style>
        <p><a href=\"/\">← Dashboard</a></p><pre>{report}</pre></html>""",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.get("/berichte/oerr-schlagseite", response_class=HTMLResponse)
def oerr_schlagseite_report() -> HTMLResponse:
    report = escape(OERR_SCHLAGSEITE_REPORT.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"""<!doctype html><html lang=\"de\"><meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
        <title>ÖRR-Schlagseite bei Migrationsthemen</title>
        <style>body{{max-width:920px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui;color:#18211b;background:#f5f3ec}}
        pre{{white-space:pre-wrap;font:inherit;background:white;padding:1.5rem;border-radius:12px}}a{{color:#075c45}}</style>
        <p><a href=\"/\">← Dashboard</a></p><pre>{report}</pre></html>""",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.get("/berichte/oerr-beitragszahler", response_class=HTMLResponse)
def oerr_beitragszahler_report() -> HTMLResponse:
    report = escape(OERR_BEITRAGSZAHLER_REPORT.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"""<!doctype html><html lang=\"de\"><meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
        <title>ÖRR-Framing vs. Beitragszahler</title>
        <style>body{{max-width:920px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui;color:#18211b;background:#f5f3ec}}
        pre{{white-space:pre-wrap;font:inherit;background:white;padding:1.5rem;border-radius:12px}}a{{color:#075c45}}</style>
        <p><a href=\"/\">← Dashboard</a></p><pre>{report}</pre></html>""",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.get("/berichte/oerr-vs-bevoelkerung", response_class=HTMLResponse)
def oerr_bevoelkerung_report() -> HTMLResponse:
    report = escape(OERR_BEVOELKERUNG_REPORT.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"""<!doctype html><html lang=\"de\"><meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
        <title>ÖRR-Berichterstattung vs. Bevölkerungshaltung</title>
        <style>body{{max-width:920px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui;color:#18211b;background:#f5f3ec}}
        pre{{white-space:pre-wrap;font:inherit;background:white;padding:1.5rem;border-radius:12px}}a{{color:#075c45}}</style>
        <p><a href=\"/\">← Dashboard</a></p><pre>{report}</pre></html>""",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.post("/api/analyze")
def analyze(request: AnalysisRequest) -> dict:
    result = {"local": analyze_local(request.text)}
    if request.deep:
        try:
            result["deep"] = analyze_with_model(request.text)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return result


@app.get("/api/research")
def research() -> dict:
    media = rows("media")
    codings = rows("article_codings")
    return {"media": media, "articles": rows("articles"),
            "claims": rows("claims"), "facts": rows("facts"),
            "omission_examples": rows("omission_examples"),
            "article_codings": codings,
            "coverage_events": rows("coverage_events"),
            "reach_ranking": rows("reach_ranking"),
            "sample_progress": sample_progress(media, codings),
            "media_summary": media_summary(media, codings),
            "goal_progress": goal_progress(codings),
            "reliability": reliability_report(codings)}


@app.get("/api/goal")
def goal() -> dict:
    """Fortschritt gegenüber dem Ziel: Top-30-Medien à ≥25 Artikel + alle ÖRR."""
    return goal_progress(rows("article_codings"))


@app.get("/api/research.csv")
def research_csv() -> StreamingResponse:
    """Export the auditable article-level coding table for independent analysis."""
    codings = rows("article_codings")
    fields = [
        "medium", "title", "url", "topic", "genre", "policy_score",
        "language_asymmetry", "counterposition", "context_completeness",
        "omission_risk", "factual_confidence", "access_level", "evidence_note",
    ]
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(codings)
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=journalismus-check-kodierungen.csv"},
    )
