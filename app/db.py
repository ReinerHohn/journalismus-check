from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .seed_data import ARTICLES, CLAIMS, FACTS, MEDIA, OMISSION_EXAMPLES
from .research_data import CODINGS, COVERAGE_EVENTS
from .reach_data import REACH_RANKING


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "journalismus_check.sqlite3"


SCHEMA = """
CREATE TABLE IF NOT EXISTS media (
  id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, domain TEXT,
  profile TEXT NOT NULL, profile_note TEXT NOT NULL,
  evidence TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS articles (
  id INTEGER PRIMARY KEY, medium TEXT NOT NULL, title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL, published TEXT, genre TEXT, access_status TEXT NOT NULL,
  research_status TEXT NOT NULL, summary TEXT, framing TEXT, orientation_signal TEXT,
  confidence REAL NOT NULL DEFAULT 0, source_note TEXT
);
CREATE TABLE IF NOT EXISTS claims (
  id INTEGER PRIMARY KEY, claim TEXT NOT NULL, status TEXT NOT NULL,
  assessment TEXT NOT NULL, supporting_sources TEXT NOT NULL,
  contradicting_sources TEXT NOT NULL, checked_at TEXT NOT NULL,
  topic TEXT NOT NULL DEFAULT 'Allgemein'
);
CREATE TABLE IF NOT EXISTS facts (
  id INTEGER PRIMARY KEY, topic TEXT NOT NULL, statement TEXT NOT NULL,
  value TEXT, scope TEXT NOT NULL, source_name TEXT NOT NULL, source_url TEXT NOT NULL,
  limitations TEXT NOT NULL, checked_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS omission_examples (
  id INTEGER PRIMARY KEY, pattern TEXT NOT NULL, verdict TEXT NOT NULL,
  explanation TEXT NOT NULL, required_evidence TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS article_codings (
  id INTEGER PRIMARY KEY, medium TEXT NOT NULL, title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL, topic TEXT NOT NULL, genre TEXT NOT NULL,
  policy_score INTEGER NOT NULL, language_asymmetry INTEGER NOT NULL,
  counterposition INTEGER NOT NULL, context_completeness INTEGER NOT NULL,
  omission_risk INTEGER NOT NULL, factual_confidence INTEGER NOT NULL,
  access_level TEXT NOT NULL, evidence_note TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS coverage_events (
  id INTEGER PRIMARY KEY, medium TEXT NOT NULL, title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL, published_at TEXT NOT NULL, report_stage TEXT NOT NULL,
  facts_available TEXT NOT NULL, facts_included TEXT NOT NULL,
  omission_verdict TEXT NOT NULL, source_basis TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reach_ranking (
  rank INTEGER PRIMARY KEY, label TEXT NOT NULL, media_name TEXT NOT NULL,
  grouping TEXT NOT NULL, reach_pct REAL, reach_note TEXT NOT NULL,
  reach_source TEXT NOT NULL, reach_url TEXT NOT NULL, political_note TEXT NOT NULL
);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with connect() as db:
        db.executescript(SCHEMA)
        claim_columns = {row[1] for row in db.execute("PRAGMA table_info(claims)")}
        if "topic" not in claim_columns:
            db.execute("ALTER TABLE claims ADD COLUMN topic TEXT NOT NULL DEFAULT 'Allgemein'")
        media_columns = {row[1] for row in db.execute("PRAGMA table_info(media)")}
        if "evidence" not in media_columns:
            db.execute("ALTER TABLE media ADD COLUMN evidence TEXT NOT NULL DEFAULT '[]'")
        db.execute("DELETE FROM articles WHERE url='https://www.focus.de/suche/ceuta'")
        db.executemany(
            """INSERT INTO media(name,domain,profile,profile_note,evidence) VALUES(?,?,?,?,?)
            ON CONFLICT(name) DO UPDATE SET domain=excluded.domain,
            profile=excluded.profile, profile_note=excluded.profile_note,
            evidence=excluded.evidence""",
            [(x["name"], x["domain"], x["profile"], x["profile_note"],
              json.dumps(x.get("evidence", []), ensure_ascii=False)) for x in MEDIA],
        )
        db.executemany(
            """INSERT INTO articles
            (medium,title,url,published,genre,access_status,research_status,summary,
             framing,orientation_signal,confidence,source_note)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(url) DO UPDATE SET medium=excluded.medium,title=excluded.title,
            published=excluded.published,genre=excluded.genre,
            access_status=excluded.access_status,research_status=excluded.research_status,
            summary=excluded.summary,framing=excluded.framing,
            orientation_signal=excluded.orientation_signal,confidence=excluded.confidence,
            source_note=excluded.source_note""",
            [tuple(x[k] for k in (
                "medium", "title", "url", "published", "genre", "access_status",
                "research_status", "summary", "framing", "orientation_signal",
                "confidence", "source_note"
            )) for x in ARTICLES],
        )
        db.executemany(
            """INSERT OR REPLACE INTO claims
            (id,claim,status,assessment,supporting_sources,contradicting_sources,checked_at)
            VALUES(?,?,?,?,?,?,?)""",
            [(x["id"], x["claim"], x["status"], x["assessment"],
              json.dumps(x["supporting_sources"]), json.dumps(x["contradicting_sources"]),
              x["checked_at"]) for x in CLAIMS],
        )
        topic_by_claim = {
            1: "Ceuta", 2: "Ceuta", 3: "Ceuta", 4: "Ceuta", 5: "Ceuta",
            6: "Deutsche Grenzpolitik", 7: "Deutsche Grenzpolitik",
            8: "Deutsche Grenzpolitik", 9: "Asylverfahrensrecht",
            10: "Kriminalitätsberichterstattung",
            11: "Kriminalitätsberichterstattung",
            12: "Kriminalitätsberichterstattung",
            13: "Kriminalitätsberichterstattung",
        }
        db.executemany(
            "UPDATE claims SET topic=? WHERE id=?",
            [(topic, claim_id) for claim_id, topic in topic_by_claim.items()],
        )
        db.executemany(
            """INSERT OR REPLACE INTO facts
            (id,topic,statement,value,scope,source_name,source_url,limitations,checked_at)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            [(x["id"],x["topic"],x["statement"],x["value"],x["scope"],
              x["source_name"],x["source_url"],x["limitations"],x["checked_at"])
             for x in FACTS],
        )
        db.executemany(
            """INSERT OR REPLACE INTO omission_examples
            (id,pattern,verdict,explanation,required_evidence) VALUES(?,?,?,?,?)""",
            [(x["id"],x["pattern"],x["verdict"],x["explanation"],x["required_evidence"])
             for x in OMISSION_EXAMPLES],
        )
        db.executemany(
            """INSERT INTO article_codings
            (medium,title,url,topic,genre,policy_score,language_asymmetry,
             counterposition,context_completeness,omission_risk,factual_confidence,
             access_level,evidence_note) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(url) DO UPDATE SET medium=excluded.medium,title=excluded.title,
            topic=excluded.topic,genre=excluded.genre,policy_score=excluded.policy_score,
            language_asymmetry=excluded.language_asymmetry,
            counterposition=excluded.counterposition,
            context_completeness=excluded.context_completeness,
            omission_risk=excluded.omission_risk,
            factual_confidence=excluded.factual_confidence,
            access_level=excluded.access_level,evidence_note=excluded.evidence_note""",
            CODINGS,
        )
        db.executemany(
            """INSERT INTO coverage_events
            (medium,title,url,published_at,report_stage,facts_available,facts_included,
             omission_verdict,source_basis) VALUES(?,?,?,?,?,?,?,?,?)
            ON CONFLICT(url) DO UPDATE SET medium=excluded.medium,title=excluded.title,
            published_at=excluded.published_at,report_stage=excluded.report_stage,
            facts_available=excluded.facts_available,facts_included=excluded.facts_included,
            omission_verdict=excluded.omission_verdict,source_basis=excluded.source_basis""",
            COVERAGE_EVENTS,
        )
        db.executemany(
            """INSERT INTO reach_ranking
            (rank,label,media_name,grouping,reach_pct,reach_note,reach_source,reach_url,political_note)
            VALUES(?,?,?,?,?,?,?,?,?)
            ON CONFLICT(rank) DO UPDATE SET label=excluded.label,
            media_name=excluded.media_name,grouping=excluded.grouping,
            reach_pct=excluded.reach_pct,reach_note=excluded.reach_note,
            reach_source=excluded.reach_source,reach_url=excluded.reach_url,
            political_note=excluded.political_note""",
            [(x["rank"], x["label"], x["media_name"], x["group"], x["reach_pct"],
              x["reach_note"], x["reach_source"], x["reach_url"], x["political_note"])
             for x in REACH_RANKING],
        )


def rows(table: str) -> list[dict]:
    if table not in {"media", "articles", "claims", "facts", "omission_examples", "article_codings", "coverage_events", "reach_ranking"}:
        raise ValueError("unknown table")
    order_column = "rank" if table == "reach_ranking" else "id"
    with connect() as db:
        result = [dict(row) for row in db.execute(f"SELECT * FROM {table} ORDER BY {order_column}")]
    if table == "claims":
        for row in result:
            row["supporting_sources"] = json.loads(row["supporting_sources"])
            row["contradicting_sources"] = json.loads(row["contradicting_sources"])
    if table == "media":
        for row in result:
            row["evidence"] = json.loads(row["evidence"] or "[]")
    return result
