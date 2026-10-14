import imaplib # Modul aus der Standardbibliothek, spricht IMAP mit Mail-Servern (Verbinden, Mails abrufen).
import os # Um Daten aus den Umgebungsvariablen zu importieren.
import mail_tools # Importiert die Datei mail_tools.py damit hier funktionen von mail_tools verwendet werden können.
import telegram_tools # Importiert die Datei telegram_tools.py damit hier funktionen von telegram_tools verwendet werden können.
import uid_speicher # Importiert das "Gedächnis" von dem Agenten.
from dotenv import load_dotenv # Importiert das laden aus der .env .

load_dotenv() # Läd die daten aus der .env in die Umgebungvariablen.

MAIL_PASSWORD = os.environ["MAIL_PASSWORD"] # Holt das Mail-Passwort aus der .env.
MAIL_USER = os.environ["MAIL_USER"] # Holt den Mail-Username aus der .env.
IMAP_SERVER = "imap.gmail.com" # Legt den Mail-Anbieter fest (in dem fall G-Mail).
IMAP_PORT = 993 # Legt den Port fest, 993 ist der Port für IMAP mit Verschlüsselung(SSL).

connection = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) # Baut eine verschlüsselte verbindung zum Mail-Server auf.
login_status, login_data = connection.login(MAIL_USER, MAIL_PASSWORD) # Loggt dich mit den Daten in deinen Account ein und gibt Status(login_status) und die Antwort der Servers(login_data) zurück.
select_status, select_data = connection.select("inbox", readonly=True) # Wählt aus von wie (readonly) und wo (inbox) gelesen wird.

last_uid = uid_speicher.load_last_uid() # Lädt die letzte UID der letzten Mail die ausgelesen wurde.
new_id = mail_tools.get_new_message_id(connection, last_uid) # Besorgt die UID's die neuer sind als die zuletzt gespeicherte.

for message_id in new_id: # Für jede UID in new_id passiert folgendes:
    raw_bytes = mail_tools.fetch_raw_bytes(connection, message_id) # Holt die rohen Bytes einer Mail.
    message = mail_tools.bytes_to_message(raw_bytes) # Macht aus den rohen Bytes ein Mail-Objekt.
    attachment_names = mail_tools.get_attachment_names(message) # Holt die Dateinamen der Anhänge als Liste. Die Anhänge selbst werden nirgends gespeichert oder geöffnet.
    message_text = mail_tools.get_message_text(message) # Holt die tatsächliche Mail-Nachricht.

    # Sendet eine Nachricht mit Absender, Betreff, Inhalt und die Namen der Anhänge an Telegram. In send_error ist entweder None(wenn alles klappt) oder ein Fehlertext(bei einem Fehler).
    send_error = telegram_tools.send_telegram_message(
        f"Neue Email erhalten\n"
        f"Von: {message['From']}\n"
        f"Betreff:\n{message['Subject']}\n"
        f"Inhalt:\n{message_text}\n"
        f"Anhänge:\n{', '.join(attachment_names)}"
    )
    # Wenn send_error einen Fehlercode enthält wird er ausgegeben im Terminal.
    if send_error is not None:
        print(send_error)

if len(new_id) >= 1: # Wenn die länge der liste new_id länger oder gleich 1 ist. Ohne diese Zeile würde der Agent ohne neue Mails crashen.
    uid_numbers = [int(uid) for uid in new_id] # Wandelt alle UID's in new_ids mit int() ind Ganzzahlen um.
    highest_uid = max(uid_numbers) # Ordnet die gröste UID zu.
    uid_speicher.save_last_uid(highest_uid) # Speichert die größte als letzte UID.

connection.close() # Schließt die zureit ausgewählte Mailbox.
connection.logout() # Beendet die vebindung zum Mail-Server.