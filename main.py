import json
import os

# Name der Datei, in der wir die Noten speichern
DATEINAME = "noten.json"

# Liste, in der wir alle Noten speichern (im Speicher)
noten = []


# ---------------- Hilfsfunktionen ----------------

def bestaetigen(frage: str) -> bool:
    """Einfache Ja/Nein-Abfrage in der Konsole."""
    while True:
        antwort = input(frage + " (j/n): ").strip().lower()
        if antwort in ("j", "ja"):
            return True
        if antwort in ("n", "nein"):
            return False
        print("Bitte 'j' oder 'n' eingeben.")


def input_float(prompt: str) -> float:
    """Fragt eine Kommazahl ab und wiederholt bei Fehlern."""
    while True:
        roh = input(prompt).replace(",", ".").strip()
        try:
            return float(roh)
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")


# ---------------- Datei-Funktionen ----------------

def daten_laden() -> list:
    """Lädt Noten aus der JSON-Datei. Gibt eine Liste zurück."""
    if not os.path.exists(DATEINAME):
        print("Keine bestehende Datei gefunden. Starte ohne gespeicherte Noten.")
        return []

    try:
        with open(DATEINAME, "r", encoding="utf-8") as f:
            daten = json.load(f)
        if isinstance(daten, list):
            # Ältere Einträge ohne 'profil' als Schule annehmen
            for eintrag in daten:
                if "profil" not in eintrag:
                    eintrag["profil"] = "schule"
            print(f"{len(daten)} Noten wurden aus '{DATEINAME}' geladen.")
            return daten
        else:
            print("Dateiformat ungültig. Starte mit leerer Liste.")
            return []
    except (OSError, json.JSONDecodeError) as e:
        print(f"Fehler beim Laden der Datei: {e}")
        print("Starte mit leerer Liste.")
        return []


def daten_speichern():
    """Speichert die aktuelle Notenliste in die JSON-Datei."""
    try:
        with open(DATEINAME, "w", encoding="utf-8") as f:
            json.dump(noten, f, ensure_ascii=False, indent=2)
        print(f"✅ Noten wurden in '{DATEINAME}' gespeichert.")
    except OSError as e:
        print(f"Fehler beim Speichern der Datei: {e}")


# ---------------- Noten-Funktionen ----------------

def zeige_menue():
    """Zeigt das Hauptmenü an."""
    print("\n===== GradeCalc =====")
    print("1) Note hinzufügen")
    print("2) Noten anzeigen")
    print("3) Noten speichern")
    print("4) Durchschnitt berechnen")
    print("5) Prüfungsrechner (benötigte Note)")
    print("6) Noten umrechnen (CH → DE/USA)")
    print("7) Beenden")


def profil_waehlen() -> str:
    """Fragt ab, ob Schule oder Studium verwendet wird."""
    while True:
        print("\nProfil wählen:")
        print("1) Schule (CH-Noten 1.0–6.0)")
        print("2) Studium (Punkte 0–100)")
        auswahl = input("Option (1 oder 2): ").strip()
        if auswahl == "1":
            return "schule"
        elif auswahl == "2":
            return "studium"
        else:
            print("Ungültige Eingabe. Bitte 1 oder 2 wählen.")


def note_hinzufuegen():
    """Fragt eine Note ab (mit Profil) und speichert sie in der Liste."""
    print("\n--- Neue Note hinzufügen ---")
    fach = input("Name des Fachs/Moduls: ").strip()
    if fach == "":
        print("Das Fach darf nicht leer sein.")
        return

    profil = profil_waehlen()

    # Note je nach Profil prüfen
    if profil == "schule":
        # CH-Skala 1.0–6.0
        while True:
            note_str = input("Note eingeben (CH-Skala 1.0–6.0): ").replace(",", ".").strip()
            try:
                note = float(note_str)
            except ValueError:
                print("❌ Ungültige Eingabe. Bitte eine Zahl eingeben (z. B. 4.5).")
                continue

            if note < 1.0 or note > 6.0:
                print("❌ Die Note muss zwischen 1.0 und 6.0 liegen.")
                continue

            break
    else:
        # Studium: Punkte 0–100
        while True:
            note_str = input("Punkte eingeben (0–100): ").replace(",", ".").strip()
            try:
                note = float(note_str)
            except ValueError:
                print("❌ Ungültige Eingabe. Bitte eine Zahl eingeben (z. B. 85).")
                continue

            if note < 0 or note > 100:
                print("❌ Die Punkte müssen zwischen 0 und 100 liegen.")
                continue

            break

    eintrag = {
        "fach": fach,
        "profil": profil,
        "note": note
    }
    noten.append(eintrag)
    print(f"✅ Note für '{fach}' ({profil}) wurde gespeichert.")


def noten_anzeigen():
    """Zeigt alle gespeicherten Noten an."""
    print("\n--- Gespeicherte Noten ---")
    if not noten:
        print("Es sind noch keine Noten vorhanden.")
        return

    for i, eintrag in enumerate(noten, start=1):
        profil = eintrag.get("profil", "schule")
        if profil == "schule":
            einheit = "CH-Note"
        else:
            einheit = "Punkte"
        print(f"{i}. {eintrag['fach']} | Profil: {profil} | {einheit}: {eintrag['note']}")


def durchschnitt_berechnen_profil(profil_filter):
    """Berechnet den Durchschnitt für ein bestimmtes Profil oder alle."""
    if profil_filter is None:
        gefiltert = noten
    else:
        gefiltert = [e for e in noten if e.get("profil", "schule") == profil_filter]

    if not gefiltert:
        print("Keine passenden Noten für diese Auswahl.")
        return None

    summe = sum(e["note"] for e in gefiltert)
    anzahl = len(gefiltert)
    durchschnitt = summe / anzahl

    print(f"Anzahl Noten: {anzahl}")
    print(f"Durchschnitt: {durchschnitt:.2f}")
    return durchschnitt


def durchschnitt_menue():
    """Untermenü für Durchschnittsberechnung."""
    print("\n--- Durchschnitt berechnen ---")
    print("1) Durchschnitt Schule (CH-Noten)")
    print("2) Durchschnitt Studium (Punkte)")
    print("3) Gesamtdurchschnitt (alle Einträge, gemischt)")
    auswahl = input("Option wählen (1–3): ").strip()

    if auswahl == "1":
        durchschnitt_berechnen_profil("schule")
    elif auswahl == "2":
        durchschnitt_berechnen_profil("studium")
    elif auswahl == "3":
        durchschnitt_berechnen_profil(None)
    else:
        print("Ungültige Eingabe. Bitte 1–3 wählen.")


# ---------------- Prüfungsrechner ----------------

def pruefungsrechner():
    """
    Berechnet, welche Note/Punkte in der nächsten Prüfung nötig sind,
    um eine Zielnote zu erreichen.
    """
    print("\n--- Prüfungsrechner: benötigte Note/Punkte ---")
    profil = profil_waehlen()

    # aktueller Durchschnitt
    aktueller = input_float("Aktueller Durchschnitt (z. B. 4.5 oder 82): ")

    # Zielnote
    ziel = input_float("Zielnote/Zielpunkte: ")

    # Gewichtung der nächsten Prüfung
    while True:
        gewicht = input_float("Gewichtung der nächsten Prüfung (0–1, z. B. 0.4): ")
        if gewicht <= 0 or gewicht > 1:
            print("Die Gewichtung muss grösser als 0 und höchstens 1 sein.")
        else:
            break

    # Formel: ziel = aktueller*(1-gewicht) + benötigte*gewicht
    benoetigt = (ziel - aktueller * (1 - gewicht)) / gewicht

    if profil == "schule":
        print(f"Du brauchst etwa die Note {benoetigt:.2f} (CH-Skala 1.0–6.0).")
        if benoetigt < 1.0 or benoetigt > 6.0:
            print("⚠ Achtung: Diese Note liegt ausserhalb der CH-Skala – Ziel evtl. nicht erreichbar.")
    else:
        print(f"Du brauchst etwa {benoetigt:.2f} Punkte (0–100).")
        if benoetigt < 0 or benoetigt > 100:
            print("⚠ Achtung: Diese Punktzahl liegt ausserhalb des Bereichs 0–100 – Ziel evtl. nicht erreichbar.")


# ---------------- Notenumrechnung CH → DE/USA ----------------

def umrechnung_ch_de(ch_note: float) -> float:
    """
    Einfache, grobe Umrechnung CH-Note (1–6) in deutsches System (1–5).
    1.0 = sehr gut, 5.0 = ungenügend.
    """
    if ch_note >= 5.5:
        return 1.0
    elif ch_note >= 5.0:
        return 2.0
    elif ch_note >= 4.5:
        return 3.0
    elif ch_note >= 4.0:
        return 4.0
    else:
        return 5.0


def umrechnung_ch_usa(ch_note: float):
    """
    Einfache Umrechnung CH-Note (1–6) in US-System (Letter + GPA).
    Sehr grobe Approximation.
    """
    if ch_note >= 5.5:
        return "A", 4.0
    elif ch_note >= 5.0:
        return "B", 3.0
    elif ch_note >= 4.5:
        return "C", 2.0
    elif ch_note >= 4.0:
        return "D", 1.0
    else:
        return "F", 0.0


def noten_umrechnen():
    """Fragt eine CH-Note ab und rechnet sie nach DE und USA um."""
    print("\n--- Notenumrechnung (CH → DE/USA) ---")
    while True:
        ch = input_float("CH-Note eingeben (1.0–6.0): ")
        if ch < 1.0 or ch > 6.0:
            print("Die Note muss zwischen 1.0 und 6.0 liegen.")
        else:
            break

    de_note = umrechnung_ch_de(ch)
    us_letter, us_gpa = umrechnung_ch_usa(ch)

    print(f"\nAusgangsnote (CH): {ch:.2f}")
    print(f"≈ Deutsches System: {de_note:.1f} (1=sehr gut, 5=ungenügend)")
    print(f"≈ US-System: {us_letter} (GPA ca. {us_gpa:.1f})")


# ---------------- Hauptfunktion ----------------

def main():
    """Hauptfunktion mit Menü und Laden der Daten."""
    print("Willkommen bei GradeCalc!")

    # Beim Start fragen, ob vorhandene Daten geladen werden sollen
    if bestaetigen("Vorhandene Noten aus Datei laden?"):
        geladene_noten = daten_laden()
        noten.extend(geladene_noten)  # in unsere Liste übernehmen
    else:
        print("Starte mit leerer Notenliste.")

    # Menü-Schleife
    while True:
        zeige_menue()
        auswahl = input("Option wählen (1–7): ").strip()

        if auswahl == "1":
            note_hinzufuegen()
        elif auswahl == "2":
            noten_anzeigen()
        elif auswahl == "3":
            daten_speichern()
        elif auswahl == "4":
            durchschnitt_menue()
        elif auswahl == "5":
            pruefungsrechner()
        elif auswahl == "6":
            noten_umrechnen()
        elif auswahl == "7":
            # vor dem Beenden noch fragen, ob gespeichert werden soll
            if bestaetigen("Vor dem Beenden speichern?"):
                daten_speichern()
            print("Programm wird beendet. Auf Wiedersehen! 👋")
            break
        else:
            print("Ungültige Eingabe. Bitte erneut versuchen.")


# Startpunkt des Programms
if __name__ == "__main__":
    main()

