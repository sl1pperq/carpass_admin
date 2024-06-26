import json

users = []
cars = []
persons = []
archive = []

# OPEN FILES

try:
    with open('data/users.json', 'r') as file:
        users = json.loads(file.read())
    with open('data/cars.json', 'r') as file:
        cars = json.loads(file.read())
    with open('data/persons.json', 'r') as file:
        persons = json.loads(file.read())
    with open('data/archive.json', 'r') as file:
        archive = json.loads(file.read())
except:
    pass


def save_data():
    with open('data/users.json', 'w') as file:
        file.write(json.dumps(users, ensure_ascii=False))
    with open('data/cars.json', 'w') as file:
        file.write(json.dumps(cars, ensure_ascii=False))
    with open('data/persons.json', 'w') as file:
        file.write(json.dumps(persons, ensure_ascii=False))
    with open('data/archive.json', 'w') as file:
        file.write(json.dumps(archive, ensure_ascii=False))


# FUNCTIONS

def check_users(email, password):
    for u in users:
        if u['email'] == email:
            if u['password'] == password:
                return True
    return False


def add_car_pass(
        car_num, car_model, car_type, owner_fio, owner_why,
        comment, date_start, date_end, object_title, by, uniq_id
):
    cars.append({
        "car_num": car_num,
        "car_model": car_model,
        "car_type": car_type,
        "owner_fio": owner_fio,
        "owner_why": owner_why,
        "comment": comment,
        "date_start": date_start,
        "date_end": date_end,
        "object_title": object_title,
        "by": by,
        "id": uniq_id
    })
    save_data()


def add_person_pass(
        owner_fio, owner_why, comment, date_start, date_end,
        object_title, by, uniq_id
):
    persons.append({
        "owner_fio": owner_fio,
        "owner_why": owner_why,
        "comment": comment,
        "date_start": date_start,
        "date_end": date_end,
        "object_title": object_title,
        "by": by,
        "id": uniq_id
    })
    save_data()


def get_user_cars_by_email(email):
    car_list = []
    for c in cars:
        if c['by'] == email:
            car_list.append(c)
    return car_list


def get_user_persons_by_email(email):
    person_list = []
    for c in persons:
        if c['by'] == email:
            person_list.append(c)
    return person_list

def get_user_archive_by_email(email):
    archive_list = []
    for c in archive:
        if c['by'] == email:
            archive_list.append(c)
    return archive_list


def get_car_by_id(id):
    for c in cars:
        if c['id'] == id:
            return c
    return KeyError


def get_person_by_id(id):
    for c in persons:
        if c['id'] == id:
            return c
    return KeyError


def delete_car_pass(id):
    for c in cars:
        if c['id'] == id:
            archive.append(c)
            cars.remove(c)
            save_data()


def delete_person_pass(id):
    for c in persons:
        if c['id'] == id:
            archive.append(c)
            persons.remove(c)
            save_data()

def make_actual(id):
    for a in archive:
        if a['id'] == id:
            archive.remove(a)
            if "car_num" in a:
                cars.append(a)
                save_data()
            else:
                persons.append(a)
                save_data()

def delete_from_archive(id):
    for a in archive:
        if a['id'] == id:
            archive.remove(a)
            save_data()