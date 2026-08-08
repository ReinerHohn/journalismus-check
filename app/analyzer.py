from __future__ import annotations

import re
from collections import Counter


LOADED_TERMS = {
    "abschottung": "wertender Begriff; kann eine restriktive Grenzpolitik negativ rahmen",
    "flüchtlingswelle": "metaphorisiert Menschen als Naturereignis",
    "invasion": "militärische Metapher für Migration",
    "illegaler": "kann den Status einer Person statt einer Handlung bezeichnen",
    "illegale": "kann den Status einer Person statt einer Handlung bezeichnen",
    "illegale migration": "rechtlich relevante, aber häufig politisch aufgeladene Kategorie",
    "willkommenskultur": "politischer Deutungsbegriff",
    "rechtspopulistisch": "politische Einordnung, die begründet oder attribuiert werden sollte",
    "linkspopulistisch": "politische Einordnung, die begründet oder attribuiert werden sollte",
    "umstritten": "unklare Zuschreibung: Wer bestreitet was?",
    "alternativlos": "schließt politische Alternativen sprachlich aus",
    "regime": "wertende Staatsbezeichnung; Kriterien sollten erkennbar sein",
    "aktivist": "Rollenbezeichnung, deren symmetrische Verwendung geprüft werden sollte",
    "hardliner": "wertende Personenbeschreibung",
}

GENERALIZERS = (
    "offensichtlich", "zweifellos", "bekanntlich", "alle", "niemand",
    "immer", "nie", "die migranten", "die bevölkerung",
)

ACTOR_PATTERN = re.compile(
    r"\b(?:[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+){0,2}|"
    r"EU|NATO|UNO|Deutschlandfunk|Bundesregierung)\b"
)


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def analyze_local(text: str) -> dict:
    sentences = _sentences(text)
    lower = text.lower()
    findings = []

    for term, note in LOADED_TERMS.items():
        for sentence in sentences:
            if term in sentence.lower():
                findings.append({
                    "category": "Framing-Begriff",
                    "term": term,
                    "quote": sentence[:500],
                    "explanation": note,
                })

    for marker in GENERALIZERS:
        for sentence in sentences:
            if re.search(rf"\b{re.escape(marker)}\b", sentence, re.I):
                findings.append({
                    "category": "Pauschalisierung",
                    "term": marker,
                    "quote": sentence[:500],
                    "explanation": "Reichweite der Aussage und Beleglage prüfen.",
                })

    actors = Counter(ACTOR_PATTERN.findall(text))
    actors = {name: count for name, count in actors.most_common(12) if len(name) > 2}
    word_count = len(re.findall(r"\b\w+\b", text, re.UNICODE))

    return {
        "word_count": word_count,
        "sentence_count": len(sentences),
        "findings": findings,
        "actors": actors,
        "questions": [
            "Welche direkt betroffenen oder verantwortlichen Akteure kommen selbst zu Wort?",
            "Sind Tatsachenbehauptungen durch benannte, überprüfbare Quellen gedeckt?",
            "Werden Ursachen und Gegenargumente mit vergleichbarer Genauigkeit dargestellt?",
            "Sind fehlende Aspekte für Thema und Veröffentlichungszeitpunkt nachweislich relevant?",
            "Werden politisch ähnliche Akteure nach denselben sprachlichen Maßstäben bezeichnet?",
        ],
        "notice": (
            "Die lokale Analyse erkennt Textmuster, aber keine Wahrheit und keine absichtliche "
            "politische Ausrichtung. Fehlende Aspekte benötigen externe Quellenprüfung."
        ),
        "signal_count": len(findings),
        "signal_density": round(len(findings) / max(word_count, 1) * 1000, 2),
    }

