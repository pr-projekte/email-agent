import imaplib
import os
import mail_tools
import telegram_tools
import uid_speicher
from dotenv import load_dotenv

load_dotenv()

MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
MAIL_USER = os.environ["MAIL_USER"]
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

connection = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
login_status, login_data = connection.login(MAIL_USER, MAIL_PASSWORD)
select_status, select_data = connection.select("inbox", readonly=True)

last_uid = uid_speicher.load_last_uid()
new_id = mail_tools.get_new_message_id(connection, last_uid)

for message_id in new_id:
    raw_bytes = mail_tools.fetch_raw_bytes(connection, message_id)
    message = mail_tools.bytes_to_message(raw_bytes)
    attachment_names = mail_tools.get_attachment_names(message)
    message_text = mail_tools.get_message_text(message)

    send_error = telegram_tools.send_telegram_message(
        f"Neue Email erhalten\n"
        f"Von: {message['From']}\n"
        f"Betreff:\n{message['Subject']}\n"
        f"Inhalt:\n{message_text}\n"
        f"Anhänge:\n{', '.join(attachment_names)}"
    )
    if send_error is not None:
        print(send_error)

if len(new_id) >= 1:
    uid_numbers = [int(uid) for uid in new_id]
    highest_uid = max(uid_numbers)
    uid_speicher.save_last_uid(highest_uid)

connection.close()
connection.logout()