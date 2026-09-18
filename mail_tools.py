import email
import email.policy


def fetch_raw_bytes(imap_connection, message_id):
    fetch_status, fetch_response = imap_connection.uid('FETCH', message_id, "(RFC822)")
    raw_bytes = fetch_response[0][1]
    return raw_bytes


def get_new_message_id(imap_connection, last_uid):
    suche = f"UID {last_uid + 1}:*"
    search_status, new_message_uid = imap_connection.uid('SEARCH', None, suche)
    uid_list = new_message_uid[0].decode().split()

    auswahl = []
    for eintrag in uid_list:
        if int(eintrag) > last_uid:
            auswahl.append(eintrag)
    return auswahl


def bytes_to_message(raw_bytes):
    message = email.message_from_bytes(raw_bytes, policy=email.policy.default)
    return message


def get_message_text(message):
    body_part = message.get_body(preferencelist=("plain", "html"))
    if body_part is None or body_part.get_content().strip() == "":
        text = "Kein Textinhalt in der Email gefunden."
    else:
        text = body_part.get_content()
    return text


def get_attachment_names(message):
    names = []
    for attachment in message.iter_attachments():
        filename = attachment.get_filename("unbenannt")
        names.append(filename)
    return names