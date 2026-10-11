# Changelog

Alle wichtigen Änderungen an diesem Projekt, die neueste Version oben.


## v0.2.0 – 11.10.2026

Das Urteil ist gebaut und gemessen. Im Agenten selbst ist es noch nicht eingebaut.

### Neu

- `evaluate.py`: Ein Sprachmodell (lokal über Ollama) bestimmt zu jeder Test-Mail eine Kategorie und eine Aktion und vergleicht beides mit Soll-Werten.
- Neun Kategorien (Mieteranfrage, Mangel/Beschwerden, Rechnung, Dienstleister, Behörde, Bewerbung, Werbung, Betrugsverdacht, Sonstiges) und vier Aktionen (sofort, heute, zur Kenntnis, ignorieren). Bei Betrugsverdacht setzt eine feste Regel die Aktion „prüfen“, nicht das Modell.
- `kategorien.json`: Kategorien, Aktionen, Vorrang-Regeln, Entscheidungsweg und Beispiele stehen in der Konfiguration, nicht im Code. Der Prompt wird daraus zusammengesetzt.
- Sicherheit pro Urteil aus den Token-Wahrscheinlichkeiten. Liegt sie unter der Schwelle 0.8, wird das Urteil als „unsicher“ markiert.
- Die Antwort des Modells wird geprüft: Kaputtes JSON, fehlende Felder oder Werte, die nicht auf der Liste stehen, landen als „ungültig“ statt als neue Kategorie.
- Zähler „fälschlich ignoriert“ für Mails, bei denen etwas zu tun ist und die trotzdem bei „ignorieren“ landen.
- Testsätze: Übungssatz (102 Mails), Prüfsatz (115 Mails) und zwei Mails mit eingeschleusten Anweisungen.

### Ergebnis

Prüfsatz, ein Lauf am 11.10.2026: Kategorie 102/115 · Aktion 96/115 · fälschlich ignoriert 0 · Betrug erkannt 12/16. Den eingeschleusten Anweisungen ist das Modell in keinem der beiden Fälle gefolgt. Messbedingungen und Details stehen in der README unter „Testsätze“.

### Bekannte Grenzen

- 4 von 16 Betrugsmails im Prüfsatz wurden nicht erkannt: zwei ohne eines der Warnzeichen, die der Prompt kennt, zwei, die wie automatische Systemnachrichten aussehen.
- Bei Schadensmeldungen stimmt die Aktion nur in 6 von 15 Fällen: meist „sofort“, wo „heute“ reicht, zweimal „heute“, wo „sofort“ nötig wäre.
- An der Grenze zwischen „heute“ und „zur Kenntnis“ wählt das Modell manchmal „zur Kenntnis“, obwohl etwas zu tun ist.
- Mit einem Cloud-Modell ist noch nichts gemessen.


## v0.1.0 – 18.09.2026

Erste lauffähige Fassung.

- Prüft ein E-Mail-Postfach per IMAP (voreingestellt ist Gmail) und schickt für jede neue E-Mail eine Telegram-Nachricht mit Absender, Betreff, Text und den Namen der Anhänge.
- Merkt sich die zuletzt übermittelte E-Mail, damit keine doppelt gemeldet wird.
- Zugangsdaten in einer `.env`, Vorlage in `.env.example`.
- README mit Screenshot, Einrichtung und Startanleitung, MIT-Lizenz.
