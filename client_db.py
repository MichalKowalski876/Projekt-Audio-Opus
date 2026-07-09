import json

FILE = "clients.json"


def load_clients():
    with open(FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_clients(data):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def client_add():
    name = input("Podaj nazwę: ")
    cut = input("Podaj część: ")

    data = load_clients()

    data.append({
        "name": name,
        "cut": cut
    })

    save_clients(data)
    print("Klient został dodany.")


def client_delete():
    name = input("Podaj nazwę: ")

    data = load_clients()

    for client in data:
        if client["name"] == name:
            data.remove(client)
            save_clients(data)
            print("Klient został usunięty.")
            return

    print("Nie znaleziono klienta.")


def client_modify():
    name = input("Podaj nazwę klienta do modyfikacji: ")

    data = load_clients()

    for client in data:
        if client["name"] == name:
            client["name"] = input("Podaj nową nazwę: ")
            client["cut"] = input("Podaj nową część: ")

            save_clients(data)
            print("Dane klienta zostały zmienione.")
            return

    print("Nie znaleziono klienta.")


def client_show():
    data = load_clients()

    print("Lista klientów:")
    for client in data:
        print(f"Nazwa: {client['name']}, Cut: {client['cut']}")
