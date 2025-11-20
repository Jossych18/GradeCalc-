# GradeCalc – Interaktiver Notenrechner

**GradeCalc** ist eine einfache, interaktive Python-Konsolenanwendung zur Verwaltung und Berechnung von Noten für Schüler*innen und Student*innen. Die Anwendung unterstützt verschiedene Profile (Schule / Studium), berechnet Durchschnitte, hilft bei der Planung von Prüfungen (Prüfungsrechner) und bietet eine einfache Umrechnung von Schweizer Noten in deutsche und US-Notenskalen.

## Funktionen

- **Noten erfassen**
  - Profilwahl:  
    - Schule: Schweizer Notenskala 1.0–6.0 (mit Validierung)  
    - Studium: Punktesystem 0–100 (mit Validierung)
  - Eingabe von Fach/Modul und Note/Punkten
  - Speicherung in einer internen Liste und bei Bedarf in einer JSON-Datei

- **Noten anzeigen**
  - Übersicht aller erfassten Noten mit Profil (Schule/Studium)
  - Ausgabe im Konsolenformat

- **Durchschnitt berechnen**
  - Durchschnitt nur für **Schule** (CH-Noten)
  - Durchschnitt nur für **Studium** (Punkte)
  - Gesamtdurchschnitt über alle erfassten Einträge

- **Prüfungsrechner (Zielnote)**
  - Eingabe des aktuellen Durchschnitts
  - Eingabe einer gewünschten Zielnote bzw. Zielpunkte
  - Eingabe der Gewichtung der nächsten Prüfung (0–1)
  - Berechnung, welche Note/Punkte in der nächsten Prüfung ungefähr erreicht werden müssen, um die Zielnote zu erreichen
  - Hinweis, falls die benötigte Note ausserhalb des gültigen Bereichs liegt (nicht realistisch erreichbar)

- **Notenskalen-Umrechnung (CH → DE/USA)**
  - Eingabe einer Schweizer Note (1.0–6.0)
  - Einfache, grobe Umrechnung:
    - in das **deutsche System** (1.0 = sehr gut, 5.0 = ungenügend)
    - in das **US-System** (Letter Grade A–F mit ungefährer GPA-Angabe)

- **Dateiverarbeitung**
  - Speichern aller Noten in einer JSON-Datei (`noten.json`)
  - Laden vorhandener Noten beim Programmstart (optional)
  - Fehlerbehandlung bei ungültigen oder fehlenden Dateien

## Technische Umsetzung

Die Anwendung ist in **Python** implementiert und verwendet:

- Datentypen: `str`, `float`, `list`, `dict`
- Kontrollstrukturen: `if/elif/else`, `while`-Schleifen, `for`-Schleifen
- Funktionen zur Strukturierung des Codes (z. B. `note_hinzufuegen()`, `durchschnitt_menue()`, `pruefungsrechner()`)
- Einfache Fehlerbehandlung via `try/except` beim Parsen von Zahlen und beim Laden/Speichern von JSON-Dateien
- Dateiverarbeitung mit `open()`, `json.load()`, `json.dump()` und Prüfung mit `os.path.exists()`

## Bedienung

1. Programm starten:

   ```bash
   python main.py
 