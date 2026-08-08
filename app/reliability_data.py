"""Blinde Zweitkodierungen (Intercoder-Reliabilität) je Medium.

Zu jedem Medium mit reifem Richtungsbefund werden die redaktionellen Volltexte ein
zweites Mal unabhängig kodiert. Die Zweitkodierer erhalten nur die Artikel-URLs und
dasselbe Kodierraster – nicht die Erstkodierung. So lässt sich prüfen, ob der
Befund von einer einzelnen Kodierung abhängt oder stabil ist.

``CODER2_BY_MEDIUM`` bildet je Medium eine Abbildung Artikel-URL -> Zweitwerte
(policy_score, language_asymmetry, counterposition, context_completeness,
omission_risk, factual_confidence). Die Erstwerte stehen in ``article_codings``;
der Vergleich (Übereinstimmung, mittlere Abweichung, gewichtetes Kappa,
Richtungsstabilität) wird in ``app/main.py`` berechnet.
"""

CODER2_LABEL = "Blinde Zweitkodierung durch unabhängige Kodierer, 8. August 2026"
CODER2_SCALE = "policy_score −2 (migrationsliberal) … +2 (migrationsrestriktiv)"

_TON = "https://www.t-online.de/nachrichten"
_ZDF = "https://www.zdfheute.de/politik"

CODER2_BY_MEDIUM = {
    "t-online": {
        f"{_TON}/deutschland/innenpolitik/id_100750950/merz-asylplaene-durch-urteil-in-frage-gestellt-was-folgt-nun-.html": (-1, 1, 2, 2, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_100741634/dobrindts-grenzkontrollen-so-sieht-der-alltag-der-bundespolizei-aus.html": (-1, 1, 1, 2, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_101073140/migration-asylantraege-halbiert-wirkt-dobrindts-migrationswende-.html": (-1, 1, 2, 2, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_101246432/migrationswende-dobrindt-feiert-erfolg-doch-asylpolitik-bleibt-baustelle.html": (-1, 1, 2, 2, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_101291086/geas-startet-warum-dobrindts-image-kratzer-bekommt.html": (-1, 1, 2, 2, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_100807796/dobrindts-migrationspolitik-das-will-die-regierung-diese-woche-erreichen.html": (0, 0, 2, 2, 0, 2),
        f"{_TON}/deutschland/innenpolitik/id_100761810/migration-spd-ministerin-behrens-fordert-abschiebefluege-nach-afghanistan.html": (1, 1, 1, 1, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_100802004/abschiebungen-nach-afghanistan-dobrindt-will-mit-taliban-sprechen.html": (1, 1, 0, 1, 2, 2),
        f"{_TON}/deutschland/innenpolitik/id_100871898/abschiebung-nach-syrien-wackeln-dobrindt-plaene-.html": (-1, 0, 2, 2, 0, 1),
        f"{_TON}/panorama/kriminalitaet/id_100678864/messerangriffe-die-taetergruppe-faellt-besonders-auf-.html": (-1, 0, 2, 2, 0, 2),
        f"{_TON}/deutschland/innenpolitik/id_100501710/gruenen-politiker-erik-marquardt-zu-migration-das-ist-absurd-.html": (-2, 2, 1, 1, 2, 1),
        f"{_TON}/tagesanbruch/id_100586550/migrationspolitik-der-union-und-afd-wohin-soll-das-fuehren-.html": (-2, 2, 1, 1, 2, 2),
        f"{_TON}/id_90794386/tagesanbruch-die-falsche-angst-vor-der-migration.html": (-2, 2, 0, 1, 2, 1),
        f"{_TON}/deutschland/innenpolitik/id_100947350/turbo-einbuergerung-vor-dem-aus-gruene-kritisieren-spd-rueckzug.html": (-1, 1, 1, 1, 2, 2),
        f"{_TON}/deutschland/innenpolitik/id_100713328/migration-merz-plant-nationale-notlage-fuer-schaerfere-grenzkontrollen.html": (1, 1, 1, 1, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_100723432/migration-das-erwarten-die-deutschen-von-merz-und-schwarz-rot.html": (1, 0, 1, 1, 1, 2),
        f"{_TON}/id_84057272/tagesanbruch-fluechtlinge-und-asylstreit-es-gibt-keinen-plan-b.html": (0, 1, 1, 2, 1, 2),
        f"{_TON}/id_84862188/tagesanbruch-migrationsdebatte-krim-krise-kommen-wir-nun-zu-etwas-anderem.html": (-1, 1, 1, 1, 1, 1),
        f"{_TON}/tagesanbruch/id_100264816/fluechtlinge-in-deutschland-jetzt-versucht-sich-olaf-scholz-als-maulheld.html": (-1, 1, 1, 2, 1, 2),
        f"{_TON}/deutschland/innenpolitik/id_100172068/migrationsforscher-warnt-das-wird-den-frust-weiter-schueren-.html": (-1, 1, 1, 2, 1, 2),
        f"{_TON}/id_83968208/tagesanbruch-die-loesung-fuer-den-asylstreit-milliarden-fuer-die-ruestung-internet-in-gefahr-.html": (-2, 2, 0, 1, 2, 2),
    },
    "ZDF": {
        f"{_ZDF}/deutschland/faktencheck-dobrindt-migrationswende-asylzahlen-100.html": (-1, 1, 2, 2, 0, 2),
        f"{_ZDF}/grenzkontrollen-beschluss-urteil-berlin-merz-dobrindt-100.html": (-1, 1, 2, 2, 1, 2),
        f"{_ZDF}/deutschland/grenzkontrolle-zurueckweisung-asyl-urteil-rechtswidrig-100.html": (-1, 0, 1, 2, 1, 2),
        f"{_ZDF}/deutschland/illner-asylverfahren-notlage-dobrindt-faktencheck-100.html": (-1, 1, 2, 2, 1, 2),
        f"{_ZDF}/deutschland/syrien-abschiebung-buergerkrieg-afghanistan-100.html": (1, 1, 0, 1, 2, 2),
        f"{_ZDF}/deutschland/bezahlkarte-asylbewerber-nrw-100.html": (-1, 1, 2, 1, 1, 2),
        f"{_ZDF}/deutschland/lanz-huber-migration-asyl-100.html": (0, 1, 2, 2, 1, 2),
        f"{_ZDF}/deutschland/kanzlerduell-scholz-merz-faktencheck-100.html": (0, 0, 2, 2, 1, 2),
        f"{_ZDF}/deutschland/auslaender-kriminalitaet-studie-ifo-polizeiliche-kriminalstatistik-100.html": (-1, 1, 1, 1, 2, 2),
        f"{_ZDF}/deutschland/schlagabtausch-wahl-faktencheck-100.html": (0, 0, 2, 2, 1, 2),
        f"{_ZDF}/deutschland/abschiebung-deutschland-integration-asyl-100.html": (-1, 1, 2, 1, 1, 2),
        f"{_ZDF}/ausland/eu-parlament-abschiebung-drittstaaten-100.html": (0, 0, 2, 2, 0, 2),
        f"{_ZDF}/afghanistan-rueckkehrer-flieger-ortskraefte-aufnahmeprogramm-100.html": (0, 0, 1, 2, 1, 2),
        f"{_ZDF}/deutschland/afghanistan-aufnahmeprogramm-bundesregierung-klage-100.html": (-1, 1, 2, 2, 1, 2),
        f"{_ZDF}/deutschland/afghanistan-aufnahme-verfassungsgericht-visa-urteil-100.html": (-1, 1, 1, 1, 1, 2),
        f"{_ZDF}/deutschland/merz-stadtbild-debatte-strassenumfrage-100.html": (-2, 2, 1, 1, 2, 2),
        f"{_ZDF}/deutschland/politbarometer-merz-stadtbild-wehrdienst-losverfahren-100.html": (1, 0, 1, 2, 1, 2),
        f"{_ZDF}/deutschland/landraetin-dickes-abschiebungen-asyl-bad-kreuznach-100.html": (2, 2, 0, 1, 2, 2),
    },
}
