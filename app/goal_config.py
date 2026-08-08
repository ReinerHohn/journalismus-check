"""Zieldefinition für die medienweite Migrations-Schlagseitenanalyse.

Das Forschungsziel ist auditierbar formuliert:

  (A) Für jedes der 30 größten deutschen Nachrichtenmedien liegen mindestens
      ``TARGET_ARTICLES`` (25) nach politischer Migrationshaltung analysierte
      Artikel vor.
  (B) Alle öffentlich-rechtlichen Online-Auftritte sind erfasst, weil der ÖRR
      über den Rundfunkbeitrag von faktisch allen Haushalten finanziert wird und
      deshalb vollständig – nicht nur in Stichproben auffälliger Anstalten –
      geprüft werden soll.

Die 30-größten-Liste ist eine belegte Reichweiten-/Auflagenauswahl (Reuters
Institute Digital News Report 2025 für Deutschland, ergänzt um auflagen- und
debattenstarke überregionale Titel, die im DNR-Markenchart nicht einzeln
ausgewiesen sind). Reine Aggregations- oder Unterhaltungsmarken ohne eigene
redaktionelle Linie sind bewusst nicht aufgenommen; jede gelistete Marke
produziert eigenständige Migrationsberichterstattung und ist damit kodierbar.
"""

TARGET_ARTICLES = 25

# (A) Die 30 größten deutschen Nachrichtenmedien (Reichweite/Auflage 2025).
# ``name`` matcht den Eintrag in MEDIA. ``kind`` = 'oerr' | 'privat'.
TOP30 = [
    {"rank": 1,  "name": "tagesschau.de",      "brand": "ARD / tagesschau",       "kind": "oerr"},
    {"rank": 2,  "name": "ZDF",                 "brand": "ZDF / heute",            "kind": "oerr"},
    {"rank": 3,  "name": "n-tv",                "brand": "RTL / ntv",              "kind": "privat"},
    {"rank": 4,  "name": "t-online",            "brand": "t-online",               "kind": "privat"},
    {"rank": 5,  "name": "BILD",                "brand": "Bild",                   "kind": "privat"},
    {"rank": 6,  "name": "WELT",                "brand": "WELT",                   "kind": "privat"},
    {"rank": 7,  "name": "DER SPIEGEL",         "brand": "Der Spiegel",            "kind": "privat"},
    {"rank": 8,  "name": "FOCUS",               "brand": "Focus",                  "kind": "privat"},
    {"rank": 9,  "name": "Die ZEIT",            "brand": "Die Zeit / ZEIT Online", "kind": "privat"},
    {"rank": 10, "name": "Süddeutsche Zeitung", "brand": "Süddeutsche Zeitung",    "kind": "privat"},
    {"rank": 11, "name": "FAZ",                 "brand": "F.A.Z.",                 "kind": "privat"},
    {"rank": 12, "name": "stern",               "brand": "stern",                  "kind": "privat"},
    {"rank": 13, "name": "Tagesspiegel",        "brand": "Der Tagesspiegel",       "kind": "privat"},
    {"rank": 14, "name": "Handelsblatt",        "brand": "Handelsblatt",           "kind": "privat"},
    {"rank": 15, "name": "taz",                 "brand": "taz",                    "kind": "privat"},
    {"rank": 16, "name": "Berliner Zeitung",    "brand": "Berliner Zeitung",       "kind": "privat"},
    {"rank": 17, "name": "RND (Redaktionsnetzwerk Deutschland)", "brand": "RND", "kind": "privat"},
    {"rank": 18, "name": "Frankfurter Rundschau", "brand": "Frankfurter Rundschau", "kind": "privat"},
    {"rank": 19, "name": "Merkur",              "brand": "Merkur.de (Ippen)",      "kind": "privat"},
    {"rank": 20, "name": "Deutschlandfunk",     "brand": "Deutschlandfunk",        "kind": "oerr"},
    {"rank": 21, "name": "WDR",                 "brand": "WDR",                    "kind": "oerr"},
    {"rank": 22, "name": "NDR",                 "brand": "NDR",                    "kind": "oerr"},
    {"rank": 23, "name": "BR",                  "brand": "Bayerischer Rundfunk",   "kind": "oerr"},
    {"rank": 24, "name": "SWR",                 "brand": "SWR",                    "kind": "oerr"},
    {"rank": 25, "name": "MDR",                 "brand": "MDR",                    "kind": "oerr"},
    {"rank": 26, "name": "RBB",                 "brand": "rbb",                    "kind": "oerr"},
    {"rank": 27, "name": "HR",                  "brand": "Hessischer Rundfunk",    "kind": "oerr"},
    {"rank": 28, "name": "Cicero",              "brand": "Cicero",                 "kind": "privat"},
    {"rank": 29, "name": "Badische Zeitung",    "brand": "Badische Zeitung",       "kind": "privat"},
    {"rank": 30, "name": "RTL",                 "brand": "RTL.de / RTL aktuell",   "kind": "privat"},
]

# (B) Alle öffentlich-rechtlichen Online-Auftritte, die vollständig erfasst sein
# sollen. ``min_articles`` ist die Zielzahl: reichweitenstarke Anstalten tragen
# das 25er-Ziel; kleine/spartige Auftritte gelten mit einer Grunderfassung als
# abgedeckt (Reifegrad bleibt transparent ausgewiesen).
OERR_ONLINE = [
    {"name": "tagesschau.de",   "brand": "ARD-aktuell / tagesschau.de", "min_articles": 25},
    {"name": "ZDF",             "brand": "ZDFheute",                    "min_articles": 25},
    {"name": "Deutschlandfunk", "brand": "deutschlandfunk.de",          "min_articles": 25},
    {"name": "WDR",             "brand": "wdr.de",                      "min_articles": 25},
    {"name": "NDR",             "brand": "ndr.de",                      "min_articles": 25},
    {"name": "BR",              "brand": "br.de",                       "min_articles": 25},
    {"name": "SWR",             "brand": "swr.de",                      "min_articles": 25},
    {"name": "MDR",             "brand": "mdr.de",                      "min_articles": 25},
    {"name": "RBB",             "brand": "rbb24.de",                    "min_articles": 25},
    {"name": "HR",              "brand": "hessenschau.de / hr.de",      "min_articles": 25},
    {"name": "SR",              "brand": "sr.de",                       "min_articles": 8},
    {"name": "Radio Bremen",    "brand": "butenunbinnen.de",            "min_articles": 8},
    {"name": "phoenix",         "brand": "phoenix.de",                  "min_articles": 8},
    {"name": "3sat",            "brand": "3sat.de (nano/Kulturzeit)",   "min_articles": 8},
    {"name": "ARTE",            "brand": "arte.tv (deutsch)",           "min_articles": 8},
]
