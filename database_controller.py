import json

FOLDER = "Databases/"


def load_database(db_name: str = "clients"):
    with open(FOLDER + db_name + ".json", "r", encoding="utf-8") as file:
        return json.load(file)


def save_database(db_name: str, data):
    with open(FOLDER + db_name + ".json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def item_add(item_data, db_name: str):
    data = load_database(db_name)
    item_data["id"] = 1 if not data else max([item["id"] for item in data]) + 1
    data.append(item_data)
    save_database(db_name, data)

def item_remove(item_id: int, db_name: str):
    data = load_database(db_name)
    for item in data:
        if item["id"] == item_id:
            data.remove(item)
            save_database(db_name, data)
            return

def item_modify(item_id: int, field: str, new_value: str, db_name: str):
    data = load_database(db_name)

    for item in data:
        if item["id"] == item_id:
            item[field] = new_value
            save_database(db_name, data)
            return

def item_get(item_id: int, db_name: str):
    data = load_database(db_name)
    for item in data:
        if item["id"] == item_id:
            return item
    return None