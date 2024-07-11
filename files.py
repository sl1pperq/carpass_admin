import json, uuid
import datetime

users = []
cars = []
persons = []
archive = []
security = []
posts = []
duty = []

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
    with open('data/security.json', 'r') as file:
        security = json.loads(file.read())
    with open('data/posts.json', 'r') as file:
        posts = json.loads(file.read())
    with open('data/duty.json', 'r') as file:
        duty = json.loads(file.read())
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
    with open('data/security.json', 'w') as file:
        file.write(json.dumps(security, ensure_ascii=False))
    with open('data/posts.json', 'w') as file:
        file.write(json.dumps(posts, ensure_ascii=False))
    with open('data/duty.json', 'w') as file:
        file.write(json.dumps(duty, ensure_ascii=False))


# FUNCTIONS

def check_users(email, password):
    for u in users:
        if u['email'] == email:
            if u['password'] == password:
                return True
    return False


def add_simple_car_pass(request, email):
    car_num = request.form.get('car_num')
    car_model = request.form.get('car_model')
    car_type = request.form.get('car_type')
    owner_fio = request.form.get('owner_fio')
    owner_why = request.form.get('owner_why')
    comment = request.form.get('comment')
    date_start = request.form.get('date_start')
    date_end = request.form.get('date_end')
    object_title = request.form.get('object_title')
    by_phone = get_user_phone(email)
    uniq_id = str(uuid.uuid4())
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
        "by": email,
        "by_phone": by_phone,
        "id": uniq_id,
        "history": []
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
            cars.remove(c)
            save_data()


def delete_person_pass(id):
    for c in persons:
        if c['id'] == id:
            persons.remove(c)
            save_data()


def auth_security(phone):
    for s in security:
        if s['phone'] == phone:
            return True
    return False


def check_for_post(num):
    for p in posts:
        print(p)
        if p['num'] == num:
            return True
    return False


def check_on_duty_by_num(num):
    for d in duty:
        if d['num'] == num:
            return d['on']


def check_on_duty_by_id(id):
    for d in duty:
        if d['id'] == id:
            return d['on']


def set_status_on_duty_by_id(id, status):
    for d in duty:
        if d['id'] == id:
            d['on'] = status
            save_data()


def check_number_plate(num):
    for c in cars:
        if c['car_num'] == num:
            return c
    return False


def get_user_phone(email):
    for u in users:
        if u['email'] == email:
            return u['phone']

def add_to_car_history(id):
    for c in cars:
        if c['id'] == id:
            c['history'].append({
                "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                "text": ""
            })