import json


def get_users_data(file):
    f = open('users.json')
    data = json.load(f)
    f.close()
    return data


def find_user(data, username, password):
    for user in data:
        if user["username"] == username and user["password"] == password:
            return user
    return False


def get_user_secret_key(data, username, password):
    for user in data:
        if user["username"] == username and user["password"] == password:
            return user["secret_key"]
        else:
            return ""


def insert_new_secret_key(user_db, user_data):
    f = open(user_db)
    data = json.load(f)
    for user in data:
        if user["username"] == user_data["username"] and user["password"] == user_data["password"]:
            user["secret_key"] = user_data["secret_key"]
    json_object = json.dumps(data)

    f.close()

    with open(user_db, "w") as outfile:
        outfile.write(json_object)

    return user_data
