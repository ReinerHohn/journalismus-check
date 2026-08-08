from __future__ import annotations

import json
import os

from openai import OpenAI


SYSTEM_PROMPT = """Du bist ein unparteiischer Medienanalyst. Analysiere ausschließlich
den vorgelegten Wortlaut. Eine politische Richtung darfst du nur als Hypothese mit
Gegenindizien nennen. Erfinde keine ausgelassenen Fakten. Unterscheide strikt:
(1) im Text beobachtbar, (2) externe Prüfung nötig, (3) nicht bestimmbar.
Bewerte linke, rechte, liberale, konservative, staatliche und aktivistische Frames
nach identischen Maßstäben. Jede Textkritik braucht ein kurzes wörtliches Zitat.
Antworte auf Deutsch als JSON mit den Schlüsseln summary, observable_findings,
missing_perspectives_to_verify, counter_indications, orientation_hypothesis,
confidence, verification_plan. observable_findings ist eine Liste aus category,
quote, analysis. confidence ist eine Zahl von 0 bis 1."""


def analyze_with_model(text: str) -> dict:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY ist nicht gesetzt")
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=SYSTEM_PROMPT,
        input=f"Analysiere diesen Artikel:\n\n{text}",
        text={"format": {"type": "json_object"}},
    )
    return json.loads(response.output_text)

