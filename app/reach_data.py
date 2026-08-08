"""Reichweiten-Ranking der größten deutschen Nachrichtenmarken.

Datengrundlage sind die belegten wöchentlichen Nutzungswerte aus dem
Reuters Institute Digital News Report 2025 – Ergebnisse für Deutschland
(Leibniz-Institut für Medienforschung / Hans-Bredow-Institut), Abbildung 15
(Offline-Marken) und Abbildung 16 (Online-Marken). ``reach_pct`` ist der höhere
der beiden ausgewiesenen Wochenreichweitenwerte (Offline oder Online); der genaue
Wortlaut steht in ``reach_note``.

Wichtig zur politischen Einordnung: Die Reichweite ist belegt. Ein politischer
*Richtungsbefund* dagegen gilt nach METHODE.md erst ab mindestens 20 volltext-
geprüften Artikeln aus mindestens drei Themenfenstern als belastbar. Deshalb wird
die politische Einordnung im Dashboard zweistufig gezeigt:

  (1) struktureller Beleg  – Eigentümer/Trägerschaft und politische Agenda,
      externe Einordnung, Selbstverständnis (Feld ``evidence`` je Medium),
  (2) Korpusbefund         – mittlerer Politikscore aus den bereits kodierten
      Migrations-/Asyl-Artikeln (Feld ``article_codings``), inklusive Fallzahl
      und Reifegrad.

``media_name`` verweist – wo vorhanden – auf den zugehörigen Eintrag in ``MEDIA``,
damit Belege und Korpusbefund im Dashboard zusammengeführt werden können. Leere
``media_name`` markieren Sammelkategorien oder Marken ohne eigene redaktionelle
Linie (z. B. Portale). ``reach_pct = None`` heißt: im DNR-2025-Markenchart nicht
einzeln ausgewiesen; die Reichweite wird dann qualitativ und quellengestützt
beschrieben.
"""

_SRC = "Reuters Institute Digital News Report 2025 – Ergebnisse für Deutschland (Leibniz-HBI), Abb. 15/16"
_URL = "https://leibniz-hbi.de/en/hbi-publications/reuters-institute-digital-news-report-2025-findings-for-germany/"

REACH_RANKING = [
    {"rank":1,"label":"ARD / Tagesschau","media_name":"tagesschau.de","group":"DNR-Einzelmarke","reach_pct":39.0,
     "reach_note":"ARD/Das-Erste-Nachrichten 39 % wöchentliche Offline-Reichweite; tagesschau.de 17 % online – die insgesamt meistgenutzte Nachrichtenmarke Deutschlands.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":2,"label":"ZDF / heute","media_name":"ZDF","group":"DNR-Einzelmarke","reach_pct":32.0,
     "reach_note":"ZDF-Nachrichten 32 % wöchentliche Offline-Reichweite; heute.de 8 % online.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":3,"label":"RTL aktuell (RTL Nachrichten)","media_name":"","group":"DNR-Einzelmarke","reach_pct":23.0,
     "reach_note":"RTL-Nachrichten 23 % wöchentliche Offline-Reichweite; reichweitenstärkstes privates TV-Nachrichtenangebot.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"Gehört zu RTL Deutschland (Bertelsmann). Kommerzieller Vollprogramm-Sender ohne ausgeprägt dokumentierte politische Linie; Nachrichten überwiegend nachrichtlich. Noch kein Migrations-Artikelkorpus im Projekt."},
    {"rank":4,"label":"n-tv","media_name":"n-tv","group":"DNR-Einzelmarke","reach_pct":18.0,
     "reach_note":"n-tv 18 % wöchentliche Offline-Reichweite; n-tv.de 13 % online.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":5,"label":"t-online","media_name":"t-online","group":"DNR-Einzelmarke","reach_pct":14.0,
     "reach_note":"t-online 14 % wöchentliche Online-Reichweite; eines der reichweitenstärksten Nachrichtenportale.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":6,"label":"Bild","media_name":"BILD","group":"DNR-Einzelmarke","reach_pct":14.0,
     "reach_note":"Bild.de 14 % wöchentliche Online-Reichweite; Bild/Bild am Sonntag 7 % offline.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":7,"label":"WELT","media_name":"WELT","group":"DNR-Einzelmarke","reach_pct":12.0,
     "reach_note":"WELT (ehem. N24) 12 % wöchentliche Offline-Reichweite; welt.de 10 % online.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":8,"label":"DER SPIEGEL","media_name":"DER SPIEGEL","group":"DNR-Einzelmarke","reach_pct":11.0,
     "reach_note":"Spiegel.de 11 % wöchentliche Online-Reichweite; Der Spiegel 7 % offline.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":9,"label":"FOCUS","media_name":"FOCUS","group":"DNR-Einzelmarke","reach_pct":10.0,
     "reach_note":"Focus Online 10 % wöchentliche Online-Reichweite; Focus 5 % offline.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":10,"label":"ProSiebenSat.1 :newstime","media_name":"","group":"DNR-Einzelmarke","reach_pct":7.0,
     "reach_note":"ProSiebenSat.1 :newstime 7 % wöchentliche Offline-Reichweite.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"Gehört zur ProSiebenSat.1-Gruppe. Kommerzielles Nachrichtenformat eines Unterhaltungssenders ohne ausgeprägt dokumentierte politische Linie. Kein Migrations-Artikelkorpus im Projekt."},
    {"rank":11,"label":"Die ZEIT / ZEIT Online","media_name":"Die ZEIT","group":"DNR-Einzelmarke","reach_pct":7.0,
     "reach_note":"ZEIT Online 7 % wöchentliche Online-Reichweite.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":12,"label":"Süddeutsche Zeitung","media_name":"Süddeutsche Zeitung","group":"DNR-Einzelmarke","reach_pct":6.0,
     "reach_note":"sueddeutsche.de 6 % wöchentliche Online-Reichweite.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":13,"label":"RTL.de","media_name":"","group":"DNR-Einzelmarke","reach_pct":5.0,
     "reach_note":"rtl.de 5 % wöchentliche Online-Reichweite.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"Digitalangebot von RTL Deutschland (Bertelsmann). Siehe RTL aktuell."},
    {"rank":14,"label":"Regionale / lokale Tageszeitungen (Sammelkategorie)","media_name":"","group":"DNR-Sammelkategorie","reach_pct":21.0,
     "reach_note":"Eine Regional- oder Lokalzeitung 21 % offline / 10 % online – zusammengenommen die reichweitenstärkste Zeitungsgattung.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"Keine Einzelmarke, sondern hunderte Titel (u. a. Badische Zeitung, Berliner Zeitung, Tagesspiegel, Frankfurter Rundschau, RND-Titel). Politische Einordnung nur je Titel sinnvoll; mehrere sind im Eigentümer-Panel einzeln belegt."},
    {"rank":15,"label":"ÖR regionale Radionachrichten (Sammelkategorie)","media_name":"","group":"DNR-Sammelkategorie","reach_pct":20.0,
     "reach_note":"Öffentlich-rechtliche regionale Radionachrichten 20 % wöchentliche Offline-Reichweite.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"Bündelt die Radioprogramme der ARD-Landesrundfunkanstalten und des Deutschlandradio/DLF. Rechtsrahmen und Auftrag sind im Eigentümer-Panel je Anstalt belegt."},
    {"rank":16,"label":"ÖR regionale TV-Nachrichten (Sammelkategorie)","media_name":"","group":"DNR-Sammelkategorie","reach_pct":19.0,
     "reach_note":"Öffentlich-rechtliche regionale TV-Nachrichten 19 % wöchentliche Offline-Reichweite.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"Bündelt die Dritten Programme der ARD (u. a. WDR, NDR, BR, MDR, SWR, rbb). Diese Anstalten sind im Eigentümer-Panel einzeln mit Rechtsrahmen belegt."},
    {"rank":17,"label":"Web.de / GMX (Nachrichtenportale)","media_name":"","group":"Portal","reach_pct":12.0,
     "reach_note":"Web.de 12 % und Gmx.net 8 % wöchentliche Online-Reichweite.","reach_source":_SRC,"reach_url":_URL,
     "political_note":"E-Mail-/Nachrichtenportale der Ströer-Tochter 7NXT bzw. United Internet; überwiegend Aggregation von Agentur- und Partnerinhalten, keine eigenständige redaktionelle politische Linie. Für eine politische Einordnung ungeeignet."},
    {"rank":18,"label":"Frankfurter Allgemeine Zeitung (FAZ)","media_name":"FAZ","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Im DNR-2025-Markenchart nicht separat ausgewiesen (unter 5 % Einzelmarken-Schwelle bzw. in Sammelkategorie Print). Bleibt eine der auflagenstärksten überregionalen Qualitätstageszeitungen.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":19,"label":"taz – die tageszeitung","media_name":"taz","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Im DNR-2025-Markenchart nicht separat ausgewiesen. Überregionale Tageszeitung mit hoher Debattenrelevanz; im Projekt bereits mit umfangreichem Artikelkorpus geprüft.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":20,"label":"Handelsblatt","media_name":"Handelsblatt","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Im DNR-2025-Markenchart nicht separat ausgewiesen. Führende deutsche Wirtschaftstageszeitung.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":21,"label":"stern","media_name":"stern","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Im DNR-2025-Markenchart nicht separat ausgewiesen. Reichweitenstarkes gesellschaftspolitisches Magazin (RTL Deutschland).","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":22,"label":"Der Tagesspiegel","media_name":"Tagesspiegel","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Als Berliner Titel Teil der Sammelkategorie 'regionale/lokale Tageszeitungen'; überregional meinungsbildend.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":23,"label":"Deutschlandfunk","media_name":"Deutschlandfunk","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Teil der Sammelkategorie 'ÖR regionale/nationale Radionachrichten' (20 %). Bundesweites wortlastiges Informationsradio; im Projekt bereits mit umfangreichem Artikelkorpus geprüft.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":24,"label":"WDR","media_name":"WDR","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Teil der Sammelkategorie 'ÖR regionale TV-/Radionachrichten' (19–20 %). Größte ARD-Landesrundfunkanstalt.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
    {"rank":25,"label":"NDR","media_name":"NDR","group":"Im DNR nicht einzeln ausgewiesen","reach_pct":None,
     "reach_note":"Teil der Sammelkategorie 'ÖR regionale TV-/Radionachrichten' (19–20 %). Verantwortet u. a. ARD-aktuell/Tagesschau.","reach_source":_SRC,"reach_url":_URL,"political_note":""},
]
