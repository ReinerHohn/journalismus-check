# Abgleich mit `../gov-data`

Stand: 8. August 2026. Die Ablage `../gov-data` wurde read-only geprüft; sie ist
keine Laufzeitabhängigkeit des Journalismus-Checks. Übernommen werden nur
nachvollziehbare Quellenverweise und klar gekennzeichnete Einschränkungen.

## Kriminalität und Staatsangehörigkeit

Die Datei `../gov-data/data/sources/kriminalitaet_pks.json` verweist auf die
BKA-PKS 2024 und unterscheidet drei Größen, die in Medien häufig vermischt
werden:

- 41,8 Prozent nichtdeutsche Tatverdächtige im Rohanteil,
- 35,4 Prozent nach Herausrechnung ausländerrechtlicher Delikte,
- 8,8 Prozent für die Kategorie „Zuwanderer“ nach dieser Bereinigung.

Die Vergleichsgröße der nichtdeutschen Wohnbevölkerung beträgt dort 14,8
Prozent. Diese Zahlen belegen eine Überrepräsentation im polizeilichen Hellfeld,
aber keine Verurteiltenquote und keine Aussage über „Migrationshintergrund“.
Die PKS zählt Tatverdächtige, nicht rechtskräftig Verurteilte; Eingebürgerte
werden als deutsch gezählt. Touristen, Durchreisende und Personen mit kurzem
Aufenthalt erschweren rohe Belastungsquoten. Alters-, Geschlechts-, Stadt- und
Lebenslagenunterschiede müssen vor jeder Kausalbehauptung geprüft werden.

Deshalb wird im Artikelraster eine Aussage wie „Marokkaner sind extrem
überrepräsentiert“ nur dann als berechenbarer Befund zugelassen, wenn Delikt,
Zeitraum, ansässiger Nenner und Vergleichsgruppe kompatibel vorliegen. Die
aktuelle Faktenbasis enthält dafür bewusst noch keine pauschale Länderquote.

Quelle: [BKA-PKS 2024](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2024/PKSTabellen/BundTVNationalitaet/bundTVNationalitaet.html).

## Einbürgerungen

`../gov-data/data/sources/einbuergerung.json` dokumentiert für 2024 insgesamt
291.955 Einbürgerungen. Die häufigsten früheren Staatsangehörigkeiten waren
Syrien (83.150), Türkei (22.525), Irak (13.545), Russland (12.980) und
Afghanistan (10.085). Diese Werte beschreiben Einbürgerungsentscheidungen,
nicht den aktuellen Zuzug und nicht die Zahl aller Personen mit
Migrationsgeschichte.

Für die reguläre Anspruchseinbürgerung werden dort § 10 StAG, B1-Sprachkenntnis,
Einbürgerungstest, Lebensunterhalt, Verfassungstreue und relevante Vorstrafen
als Prüfbedingungen dokumentiert. Im Dashboard wird deshalb ein Rekordwert
nicht als Beleg für eine erleichterte oder „automatische“ Einbürgerung gewertet.

Quelle: [Destatis, Einbürgerungen 2024](https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/06/PD25_204_125.html) und [§ 10 StAG](https://www.gesetze-im-internet.de/stag/__10.html).

## Nutzung im Mediencheck

Die Werte dienen als externe Faktenanker. Ein Artikel kann die Rohzahl korrekt
zitieren und trotzdem durch fehlenden Nenner, fehlende Deliktbereinigung oder
die Gleichsetzung von Tatverdächtigen und Verurteilten ein unvollständiges Bild
erzeugen. Umgekehrt ist das Weglassen einer Nationalität nicht automatisch ein
Auslassungsfehler: Entscheidend sind Relevanz, gesicherter Kenntnisstand zum
Veröffentlichungszeitpunkt und die Vergleichbarkeit der Statistik.
