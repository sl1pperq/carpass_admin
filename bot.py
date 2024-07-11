import time

import telebot
from config import BOT_TOKEN
from files import *
import uuid
import cv2
import pytesseract
from scanner import *

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def bot_start(msg):
    id = get_id(msg)
    print(id)
    if check_on_duty_by_id(id):
        bot.send_message(id, 'Вы уже авторизованы')
    else:
        a = bot.send_message(id, 'Введите номер своего телефона в формате: 88005553535')
        bot.register_next_step_handler(a, bot_start_num_post)


def bot_start_num_post(msg):
    id = get_id(msg)
    phone = int(msg.text)
    if auth_security(phone) == True:
        a = bot.send_message(id, 'Пришлите фото QR-кода поста, чтобы начать смену')
        bot.register_next_step_handler(a, bot_start_photo_post)
    else:
        a = bot.send_message(id, 'Такой номер не найден. Введите номер своего телефона в формате: 88005553535')
        bot.register_next_step_handler(a, bot_start_num_post)


def bot_start_photo_post(msg):
    id = get_id(msg)
    photo = msg.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    uniq_id = str(uuid.uuid4())
    save_path = f'photos/{uniq_id}.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(msg, 'Фото принято, идет обработка')
    img = cv2.imread(save_path)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    value = str(value)
    print(value)
    if value == "123456":
        bot.send_message(id, 'Теперь вы на смене и можете сканировать номера')
        set_status_on_duty_by_id(id, True)
    else:
        a = bot.send_message(id, 'Не удалось распознать фото, попробуйте еще раз')
        bot.register_next_step_handler(a, bot_start_photo_post)


@bot.message_handler(commands=['car'])
def bot_scan(msg):
    id = get_id(msg)
    if check_on_duty_by_id(id):
        a = bot.send_message(id, 'Пришлите фото номера автомобиля')
        bot.register_next_step_handler(a, bot_scan_get_car)
    else:
        bot.send_message(id, 'Вы не на смене, авторизуйтесь /start')


def bot_scan_get_car(msg):
    id = get_id(msg)
    photo = msg.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    uniq_id = str(uuid.uuid4())
    save_path = f'cars/{uniq_id}.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(msg, 'Фото принято, идет обработка')
    carplate_img_rgb = open_img(
        img_path=f'/Users/sergeysergeev2500mail.ru/carpass_admin/{save_path}'
    )
    carplate_haar_cascade = cv2.CascadeClassifier(
        f'/Users/sergeysergeev2500mail.ru/carpass_admin/haar_cascades/haarcascade_russian_plate_number.xml'
    )
    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    plt.imshow(carplate_extract_img)
    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    car_num = pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )
    print(car_num)
    if car_num:
        bot.send_message(id, f"Распознан номер: {car_num}")
        car_num = car_num.upper()
        res = check_number_plate(car_num)
        if res == False:
            bot.send_message(id, 'Пропуск на данный автомобиль не был заказан')
        else:
            text = f'Пропуск на {res["car_num"]} действует с {res["date_start"]} по {res["date_end"]} на {res["object_title"]}\n\nФИО: {res["owner_fio"]}\nПричина: {res["owner_why"]}\nКомментарий: {res["comment"]}'
            bot.send_message(id, text)
    else:
        a = bot.send_message(id, 'Пришлите номер автомобиля (слитно, английскими буквами)')
        bot.register_next_step_handler(a, handle_car_checking)


@bot.message_handler(commands=['car_text'])
def car_text(msg):
    id = get_id(msg)
    a = bot.send_message(id, 'Пришлите номер автомобиля (слитно, английскими буквами)')
    bot.register_next_step_handler(a, handle_car_checking)


def handle_car_checking(msg):
    id = get_id(msg)
    car_num = msg.text.upper()
    res = check_number_plate(car_num)
    if res == False:
        bot.send_message(id, 'Пропуск на данный автомобиль не был заказан')
    else:
        text = f'Пропуск на {res["car_num"]} действует с {res["date_start"]} по {res["date_end"]} на {res["object_title"]}\n\nФИО: {res["owner_fio"]}\nПричина: {res["owner_why"]}\nКомментарий: {res["comment"]}'
        bot.send_message(id, text)


def get_id(message):
    return message.chat.id


bot.polling()
