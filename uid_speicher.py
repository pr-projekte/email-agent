UID_DATEI = "letzte_uid.txt"


def save_last_uid(uid):
    with open(UID_DATEI, "w") as datei:
        datei.write(str(uid))


def load_last_uid():
    try:
        with open(UID_DATEI, "r") as datei:
            last_uid = datei.read()

    except FileNotFoundError:
        last_uid = 0
        with open(UID_DATEI, "w") as datei:
            datei.write(str(last_uid))

    return int(last_uid)