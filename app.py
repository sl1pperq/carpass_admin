import uuid

from flask import *
from files import *

app = Flask(__name__)
app.secret_key = 'carpass'


@app.route('/', methods=['GET'])
def main_page():
    if session.get('auth', False) == False:
        return render_template('welcome.html')
    else:
        return redirect('/dashboard')


@app.route('/', methods=['POST'])
def post_main_page():
    email = request.form.get('email')
    password = request.form.get('password')
    result = check_users(email, password)
    if result == True:
        session['auth'] = email
        return redirect('/dashboard')
    else:
        alert = 'Неправильная почта или пароль'
        return render_template('welcome.html', alert=alert)


@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    if not session.get('auth', False):
        return redirect('/')
    else:
        user_cars = get_user_cars_by_email(session['auth'])
        user_persons = get_user_persons_by_email(session['auth'])
        user_archive = get_user_archive_by_email(session['auth'])
        archive_status = request.args.get('archive')
        asc, asp = 0, 0
        if archive_status == 'car':
            asc = 1
        elif archive_status == 'person':
            asp = 1
        return render_template(
            'dashboard.html', cars=user_cars, persons=user_persons, archive=user_archive, asc=asc, asp=asp
        )


@app.route('/new_car', methods=['POST'])
def post_new_car():
    car_num = request.form.get('car_num')
    car_model = request.form.get('car_model')
    car_type = request.form.get('car_type')
    owner_fio = request.form.get('owner_fio')
    owner_why = request.form.get('owner_why')
    comment = request.form.get('comment')
    date_start = request.form.get('date_start')
    date_end = request.form.get('date_end')
    object_title = request.form.get('object_title')
    by = session['auth']
    uniq_id = str(uuid.uuid4())
    add_car_pass(
        car_num, car_model, car_type, owner_fio, owner_why, comment, date_start, date_end, object_title, by, uniq_id
    )
    return redirect('/dashboard')


@app.route('/new_person', methods=['POST'])
def post_new_person():
    owner_fio = request.form.get('owner_fio')
    owner_why = request.form.get('owner_why')
    comment = request.form.get('comment')
    date_start = request.form.get('date_start')
    date_end = request.form.get('date_end')
    object_title = request.form.get('object_title')
    by = session['auth']
    uniq_id = str(uuid.uuid4())
    add_person_pass(
        owner_fio, owner_why, comment, date_start, date_end, object_title, by, uniq_id
    )
    return redirect('/dashboard')


@app.route('/dashboard/info_car/<id>', methods=['GET'])
def get_dashboard_info_car(id):
    car = get_car_by_id(id)
    return render_template('dashboard_car.html', car=car)


@app.route('/dashboard/info_person/<id>', methods=['GET'])
def get_dashboard_info_person(id):
    person = get_person_by_id(id)
    return render_template('dashboard_person.html', p=person)


@app.route('/delete/car/<id>', methods=['GET'])
def get_delete_car(id):
    delete_car_pass(id)
    return redirect('/dashboard')


@app.route('/delete/person/<id>', methods=['GET'])
def get_delete_person(id):
    delete_person_pass(id)
    return redirect('/dashboard')

@app.route('/from_archive/<id>', methods=['GET'])
def get_from_archive(id):
    make_actual(id)
    return redirect('/dashboard')

@app.route('/max_delete/<id>', methods=['GET'])
def get_max_delete(id):
    delete_from_archive(id)
    return redirect('/dashboard')



app.run()
