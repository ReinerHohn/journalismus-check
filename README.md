# Journalismus-Check

Das dauerhafte fachliche Ziel und die zu prüfenden Hypothesen stehen in
[`PROJEKTZIEL.md`](PROJEKTZIEL.md).

Ausgearbeitete Einzelanalysen liegen im Ordner `reports/`, zunächst der
[Deutschlandfunk-Kommentar zu Ceuta](reports/dlf-ceuta-analyse.md).

Ein transparenter Prototyp zur Analyse journalistischer Texte. Das Tool sucht nicht
nach einer vorgegebenen politischen Meinung, sondern nach beobachtbaren Merkmalen:

- wertende oder politisch aufgeladene Begriffe im Wortlaut,
- unklare Zuschreibungen und pauschale Aussagen,
- Verteilung der genannten Akteure,
- Trennung von Fakten, Zitaten und Deutungen,
- mögliche Gegenperspektiven und extern zu prüfende Auslassungen.

Zusätzlich enthält das Tool einen SQLite-gestützten Medienvergleich am Fall Ceuta.
Eine erste artikelbasierte Pilotstatistik zu Ceuta und deutschen
Grenzzurückweisungen verwendet das dokumentierte Raster in [METHODE.md](METHODE.md).
Sie zeigt noch keine allgemeine Zeitungsausrichtung: Dafür sind mindestens 20
Volltexte aus drei Themenfenstern je Medium vorgesehen.

Der aktuelle Forschungsstand mit 314 Kodierungen aus neunzehn Themenfenstern ist in
[reports/medienweite-stichprobe-stand-2026-08-08.md](reports/medienweite-stichprobe-stand-2026-08-08.md)
dokumentiert.

Das vorab festgelegte ÖRR-Stichprobendesign steht in
[reports/oerr-stichprobendesign-2026-08-08.md](reports/oerr-stichprobendesign-2026-08-08.md).
Der systematische Durchgang aller ÖRR-Anbieter auf politische Schlagseite bei
Migrationsthemen – mit Genre-Trennung und Einordnung gegenüber den privaten
Polen – ist in
[reports/oerr-schlagseite-2026-08-08.md](reports/oerr-schlagseite-2026-08-08.md)
dokumentiert.
Der Abgleich mit der lokalen amtlichen Datenablage `../gov-data` ist in
[reports/gov-data-abgleich-2026-08-08.md](reports/gov-data-abgleich-2026-08-08.md)
mit Nennern, Deliktbereinigung und Quellenkritik festgehalten.
Er speichert Rechercheergebnisse dauerhaft in `data/journalismus_check.sqlite3`
und stellt sie im Dashboard nach Medium, Genre, Zugriffsstatus, Prüftiefe,
Framing, Orientierungssignal und Bewertungssicherheit gegenüber.
Die artikelgenaue Tabelle ist zusätzlich als CSV über `/api/research.csv`
exportierbar.
Das Dashboard zeigt außerdem je Medium eine Vergleichstabelle mit Volltextzahl,
Themenzahl, Orientierungsmittel und codierter Kontextlückenrate. Diese Rate ist
ein Prüfindikator und kein Beweis absichtlichen Weglassens.

## Eigenschaften des Tools

- **Quellennah:** Jeder Artikel erhält URL, Datum, Medium und Recherchehinweis.
- **Transparenter Prüfstatus:** Volltext, Metadaten, Paywall und „nicht gefunden“
  werden unterschieden. Ein ungelesener Text wird nicht als analysiert ausgegeben.
- **Genre-sensibel:** Nachricht, Analyse und Kommentar werden nicht nach demselben
  Neutralitätsmaßstab behandelt. Meinungsstärke ist noch kein Qualitätsmangel.
- **Symmetrisch:** Migrationsliberale und migrationsrestriktive Kampfbegriffe werden
  nach denselben Kriterien markiert.
- **Claim-Prüfung:** Umstrittene Aussagen werden als belegt, teilweise belegt,
  widerlegt oder offen geführt; Gegenquellen bleiben sichtbar.
- **Keine erfundenen Auslassungen:** Was im Artikel fehlt, wird zunächst als
  Recherchefrage behandelt und erst mit belastbaren externen Quellen bewertet.
- **Unsicherheit sichtbar:** Jede politische Orientierung eines Artikels bekommt
  eine Konfidenz. Die grobe Einordnung eines Mediums ist ausdrücklich nur eine
  überprüfbare Arbeitshypothese.
- **Reproduzierbar:** Der lokale Wortlisten-Check arbeitet deterministisch; eine
  optionale KI-Tiefenanalyse ist davon getrennt.
- **Datensparsam:** Artikelvolltexte fremder Verlage werden nicht ungeprüft
  vervielfältigt; gespeichert werden primär Metadaten, kurze Belege und Analysen.
- **Amtliche Gegenprüfung:** Destatis GENESIS, BKA-PKS und Bundestag-DIP bilden
  eine vom Artikel getrennte Faktenbasis. Zugangsdaten werden nur aus
  Umgebungsvariablen gelesen und nie im Repository gespeichert.
- **Saubere Personenkategorien:** Staatsangehörigkeit, Einbürgerung,
  Migrationshintergrund und Aufenthaltsstatus werden nicht gleichgesetzt.
- **Statistik mit Nenner:** Überrepräsentation wird nur berechnet, wenn Zähler,
  Bevölkerungsbasis, Zeitraum, Deliktsgruppe, Alter, Geschlecht und Ansässigkeit
  kompatibel sind. Tatverdächtige werden nicht als Verurteilte bezeichnet.

Der Ceuta-Datenbestand ist ein Recherche-Snapshot vom **8. August 2026**. Er enthält
auch Negativbefunde. Beispielsweise wurde die Behauptung, Apollo News habe die Zahl
von 7.000 verbliebenen Menschen aufgedeckt, bislang nicht bestätigt; der auffindbare
Treffer stammt von WELT. Ebenso ist „nachgewiesene Dschihadisten“ nach dem derzeitigen
Quellenstand nicht belegt, während eine Meldung das spanische Innenministerium mit
dem gegenteiligen Ergebnis zitiert. Solche Korrekturen sind Kernfunktion, keine
politische Stellungnahme.

### Korrigierter Ceuta-Gerichtsclaim

Der spanische Tribunal Supremo entschied am 8. Juli 2026 im Kern, dass die
Sonderregel der unmittelbaren Zurückweisung (`devolución en caliente`) nicht auf
Menschen angewandt werden kann, die Ceuta oder Melilla schwimmend erreichen, ohne
ein physisches Rückhalteelement zu überwinden. Das bedeutet ein reguläres
Einzelfallverfahren, nicht automatisch Asyl oder dauerhaftes Bleiberecht. Die
anschließende Verkürzung zu einer angeblich vollständig geöffneten Grenze wurde in
marokkanischen sozialen Medien verbreitet. Das Tool trennt daher Urteil,
Desinformation, möglichen Anreizeffekt und nicht bewiesene Monokausalität.

## Start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Dann <http://127.0.0.1:8000> öffnen. Ohne API-Schlüssel läuft die lokale Analyse.
Mit `OPENAI_API_KEY` wird zusätzlich eine strukturierte Tiefenanalyse angeboten.

```bash
export OPENAI_API_KEY=...
export OPENAI_MODEL=gpt-5-mini
```

## Methodische Grenze

Ein einzelner Artikel kann Framing- oder Auswahlindizien liefern, aber keine
Redaktionslinie beweisen. Dafür braucht es ein vorab definiertes Korpus, mehrere
Themen, Zeiträume, Vergleichsmedien, Blind-Codierung und dokumentierte Regeln.
Insbesondere kann eine reine Textanalyse nicht wissen, ob eine nicht erwähnte
Behauptung wahr, relevant oder zum Veröffentlichungszeitpunkt bekannt war.

## Tests

```bash
pytest
```
