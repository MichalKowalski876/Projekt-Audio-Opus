import client_db


def temp():
    mode = input("1. Dodaj klienta\n2. Usuń klienta\n3. Modyfikuj klienta\n4. Pokaż Klientów")
    if mode == "1":
        client_db.client_add()
    elif mode == "2":
        client_db.client_delete()
    elif mode == "3":
        client_db.client_modify()
    elif mode == "4":
        client_db.client_show()


if __name__ == '__main__':
    temp()
