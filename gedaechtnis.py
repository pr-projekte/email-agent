import sqlite3
import os
from datetime import datetime

ORDNER = os.path.dirname(__file__)
DB_DATEI = os.path.join(ORDNER, "gedaechtnis.db")

def tabelle_anlegen():
    verbindung = sqlite3.connect(DB_DATEI)
    cursor = verbindung.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS mails("
        "uid INTEGER PRIMARY KEY, "
        "absender TEXT, "
        "betreff TEXT, "
        "kategorie TEXT, "
        "aktion TEXT, "
        "kategorie_unsicher INTEGER, "
        "aktion_unsicher INTEGER, "
        "gespeichert_am TEXT)"
        )
    
    verbindung.commit()
    verbindung.close()


def mail_speichern(uid, absender, betreff, kategorie, aktion, kategorie_unsicher, aktion_unsicher):
    jetzt = datetime.now()
    gespeichert_am = jetzt.strftime("%Y-%m-%d %H:%M:%S")
    
    verbindung = sqlite3.connect(DB_DATEI)
    cursor = verbindung.cursor()

    cursor.execute("INSERT OR IGNORE INTO mails VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (uid, absender, betreff, kategorie, aktion, kategorie_unsicher, aktion_unsicher, gespeichert_am))

    verbindung.commit()
    verbindung.close()