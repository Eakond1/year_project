import time
import openpyxl
import telebot
from telebot import types
import json
import datetime
import schedule

bot = telebot.TeleBot('')
users = []

try:
    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.loads(file.read())
except Exception as e:
    print(e)


def save_data():
    with open('users.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(users, ensure_ascii=False))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    class_10t = types.KeyboardButton("10Т")
    class_10i = types.KeyboardButton("10И")
    markup.add(class_10t, class_10i)
    m = bot.send_message(chat_id, 'Привет! В каком ты классе?', reply_markup=markup)
    bot.register_next_step_handler(m, know_user_class)


def know_user_class(message):
    chat_id = message.chat.id
    user_class = message.text
    u = find_user(chat_id)
    if u == True:
        change_user_class(chat_id, user_class)
        bot.send_message(chat_id, 'Вы успешно изменили свой класс', reply_markup=types.ReplyKeyboardRemove())
    else:
        if user_class == "10Т" or user_class == "10И":
            users.append({
                "id": chat_id,
                "class": user_class
            })
            save_data()
            bot.send_message(chat_id, 'Вы успешно завершили регистрацию', reply_markup=types.ReplyKeyboardRemove())
        else:
            m = bot.send_message(chat_id, 'Повторите попытку')
            bot.register_next_step_handler(m, know_user_class)


@bot.message_handler(commands=['schedule'])
def start(message):
    chat_id = message.chat.id
    schedule.every().day.at("08:30").do(send_notification, chat_id)
    schedule.every().day.at("09:15").do(send_day_second, chat_id)
    schedule.every().day.at("10:10").do(send_day_third, chat_id)
    schedule.every().day.at("11:10").do(send_day_forth, chat_id)
    schedule.every().day.at("12:10").do(send_day_fifth, chat_id)
    schedule.every().day.at("13:05").do(send_day_sixth, chat_id)
    schedule.every().day.at("14:10").do(send_day_seventh, chat_id)
    schedule.every().day.at("15:15").do(send_day_eighth, chat_id)


def send_lessons(lesson, chat_id):
    for i in range(len(lesson)):
        bot.send_message(chat_id, lesson[i])
        time.sleep(1)


def get_list_of_lessons(day, user_class):
    if user_class == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        from_val = 0
        to_val = 0
        if day == 'Monday':
            from_val = 3
            to_val = 11
        elif day == 'Tuesday':
            from_val = 13
            to_val = 20
        elif day == 'Wednesday':
            from_val = 22
            to_val = 29
        elif day == 'Thursday':
            from_val = 31
            to_val = 38
        elif day == 'Friday':
            from_val = 40
            to_val = 47
        for i in range(from_val, to_val):
            num = active[f'A{i}'].value
            name = active[f'B{i}'].value
            cabinet = active[f'C{i}'].value
            teacher = active[f'D{i}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
        return lesson
    elif user_class == "10И":
        dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
        active = dataframe.active
        lesson = []
        from_val = 0
        to_val = 0
        if day == 'Monday':
            from_val = 3
            to_val = 10
        elif day == 'Tuesday':
            from_val = 12
            to_val = 20
        elif day == 'Wednesday':
            from_val = 22
            to_val = 29
        elif day == 'Thursday':
            from_val = 31
            to_val = 38
        elif day == 'Friday':
            from_val = 40
            to_val = 47
        for i in range(from_val, to_val):
            num = active[f'A{i}'].value
            name = active[f'B{i}'].value
            cabinet = active[f'C{i}'].value
            teacher = active[f'D{i}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
        return lesson


def find_user(id):
    for u in users:
        if u['id'] == id:
            return True
    return False


def get_user_class(id):
    for u in users:
        if u['id'] == id:
            return u['class']


def change_user_class(id, new_class):
    for u in users:
        if u['id'] == id:
            u['class'] = new_class
            save_data()


def send_notification(chat_id):
    print(chat_id)
    wd = datetime.datetime.today().weekday()
    if wd == 0:
        clas = get_user_class(chat_id)
        lesson = get_list_of_lessons("Monday", clas)
        bot.send_message(chat_id, 'Расписание на понедельник:')
        send_lessons(lesson, chat_id)
    elif wd == 1:
        clas = get_user_class(chat_id)
        lesson = get_list_of_lessons("Tuesday", clas)
        bot.send_message(chat_id, 'Расписание на вторник')
        send_lessons(lesson, chat_id)
    elif wd == 2:
        clas = get_user_class(chat_id)
        lesson = get_list_of_lessons("Wednesday", clas)
        bot.send_message(chat_id, 'Расписание на среду')
        send_lessons(lesson, chat_id)
    elif wd == 3:
        clas = get_user_class(chat_id)
        lesson = get_list_of_lessons("Thursday", clas)
        bot.send_message(chat_id, 'Расписание на четверг')
        send_lessons(lesson, chat_id)
    elif wd == 4:
        clas = get_user_class(chat_id)
        lesson = get_list_of_lessons("Friday", clas)
        bot.send_message(chat_id, 'Расписание на пятницу')
        send_lessons(lesson, chat_id)


def get_day_two(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{4}'].value
            name = active[f'B{4}'].value
            cabinet = active[f'C{4}'].value
            teacher = active[f'D{4}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{14}'].value
            name = active[f'B{14}'].value
            cabinet = active[f'C{14}'].value
            teacher = active[f'D{14}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{23}'].value
            name = active[f'B{23}'].value
            cabinet = active[f'C{23}'].value
            teacher = active[f'D{23}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{32}'].value
            name = active[f'B{32}'].value
            cabinet = active[f'C{32}'].value
            teacher = active[f'D{32}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{41}'].value
            name = active[f'B{41}'].value
            cabinet = active[f'C{41}'].value
            teacher = active[f'D{41}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
    elif clas == "10И":
        dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{4}'].value
            name = active[f'B{4}'].value
            cabinet = active[f'C{4}'].value
            teacher = active[f'D{4}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{13}'].value
            name = active[f'B{13}'].value
            cabinet = active[f'C{13}'].value
            teacher = active[f'D{13}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{23}'].value
            name = active[f'B{23}'].value
            cabinet = active[f'C{23}'].value
            teacher = active[f'D{23}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{32}'].value
            name = active[f'B{32}'].value
            cabinet = active[f'C{32}'].value
            teacher = active[f'D{32}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{41}'].value
            name = active[f'B{41}'].value
            cabinet = active[f'C{41}'].value
            teacher = active[f'D{41}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson


def send_day_second(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_two(clas)
    send_lesson(lesson, chat_id)


def get_day_three(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{5}'].value
            name = active[f'B{5}'].value
            cabinet = active[f'C{5}'].value
            teacher = active[f'D{5}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{15}'].value
            name = active[f'B{15}'].value
            cabinet = active[f'C{15}'].value
            teacher = active[f'D{15}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{24}'].value
            name = active[f'B{24}'].value
            cabinet = active[f'C{24}'].value
            teacher = active[f'D{24}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{33}'].value
            name = active[f'B{33}'].value
            cabinet = active[f'C{33}'].value
            teacher = active[f'D{33}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{42}'].value
            name = active[f'B{42}'].value
            cabinet = active[f'C{42}'].value
            teacher = active[f'D{42}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
    elif clas == "10И":
        dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{5}'].value
            name = active[f'B{5}'].value
            cabinet = active[f'C{5}'].value
            teacher = active[f'D{5}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{14}'].value
            name = active[f'B{14}'].value
            cabinet = active[f'C{14}'].value
            teacher = active[f'D{14}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{24}'].value
            name = active[f'B{24}'].value
            cabinet = active[f'C{24}'].value
            teacher = active[f'D{24}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{33}'].value
            name = active[f'B{33}'].value
            cabinet = active[f'C{33}'].value
            teacher = active[f'D{33}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{42}'].value
            name = active[f'B{42}'].value
            cabinet = active[f'C{42}'].value
            teacher = active[f'D{42}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson


def send_day_third(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_three(clas)
    send_lesson(lesson, chat_id)


def get_day_four(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{6}'].value
            name = active[f'B{6}'].value
            cabinet = active[f'C{6}'].value
            teacher = active[f'D{6}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{16}'].value
            name = active[f'B{16}'].value
            cabinet = active[f'C{16}'].value
            teacher = active[f'D{16}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{25}'].value
            name = active[f'B{25}'].value
            cabinet = active[f'C{25}'].value
            teacher = active[f'D{25}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{34}'].value
            name = active[f'B{34}'].value
            cabinet = active[f'C{34}'].value
            teacher = active[f'D{34}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{43}'].value
            name = active[f'B{43}'].value
            cabinet = active[f'C{43}'].value
            teacher = active[f'D{43}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
    elif clas == "10И":
        dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{6}'].value
            name = active[f'B{6}'].value
            cabinet = active[f'C{6}'].value
            teacher = active[f'D{6}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{15}'].value
            name = active[f'B{15}'].value
            cabinet = active[f'C{15}'].value
            teacher = active[f'D{15}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{25}'].value
            name = active[f'B{25}'].value
            cabinet = active[f'C{25}'].value
            teacher = active[f'D{25}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{34}'].value
            name = active[f'B{34}'].value
            cabinet = active[f'C{34}'].value
            teacher = active[f'D{34}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{43}'].value
            name = active[f'B{43}'].value
            cabinet = active[f'C{43}'].value
            teacher = active[f'D{43}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson


def send_day_forth(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_four(clas)
    send_lesson(lesson, chat_id)


def get_day_five(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{7}'].value
            name = active[f'B{7}'].value
            cabinet = active[f'C{7}'].value
            teacher = active[f'D{7}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{17}'].value
            name = active[f'B{17}'].value
            cabinet = active[f'C{17}'].value
            teacher = active[f'D{17}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{26}'].value
            name = active[f'B{26}'].value
            cabinet = active[f'C{26}'].value
            teacher = active[f'D{26}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{35}'].value
            name = active[f'B{35}'].value
            cabinet = active[f'C{35}'].value
            teacher = active[f'D{35}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{44}'].value
            name = active[f'B{44}'].value
            cabinet = active[f'C{44}'].value
            teacher = active[f'D{44}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
    elif clas == "10И":
        dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{7}'].value
            name = active[f'B{7}'].value
            cabinet = active[f'C{7}'].value
            teacher = active[f'D{7}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{16}'].value
            name = active[f'B{16}'].value
            cabinet = active[f'C{16}'].value
            teacher = active[f'D{16}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{26}'].value
            name = active[f'B{26}'].value
            cabinet = active[f'C{26}'].value
            teacher = active[f'D{26}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{35}'].value
            name = active[f'B{35}'].value
            cabinet = active[f'C{35}'].value
            teacher = active[f'D{35}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{44}'].value
            name = active[f'B{44}'].value
            cabinet = active[f'C{44}'].value
            teacher = active[f'D{44}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson


def send_day_fifth(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_five(clas)
    send_lesson(lesson, chat_id)


def get_day_six(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{8}'].value
            name = active[f'B{8}'].value
            cabinet = active[f'C{8}'].value
            teacher = active[f'D{8}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{18}'].value
            name = active[f'B{18}'].value
            cabinet = active[f'C{18}'].value
            teacher = active[f'D{18}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{27}'].value
            name = active[f'B{27}'].value
            cabinet = active[f'C{27}'].value
            teacher = active[f'D{27}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{36}'].value
            name = active[f'B{36}'].value
            cabinet = active[f'C{36}'].value
            teacher = active[f'D{36}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{45}'].value
            name = active[f'B{45}'].value
            cabinet = active[f'C{45}'].value
            teacher = active[f'D{45}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif clas == "10И":
            dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
            active = dataframe.active
            lesson = []
            if wd == 0:
                num = active[f'A{8}'].value
                name = active[f'B{8}'].value
                cabinet = active[f'C{8}'].value
                teacher = active[f'D{8}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 1:
                num = active[f'A{17}'].value
                name = active[f'B{17}'].value
                cabinet = active[f'C{17}'].value
                teacher = active[f'D{17}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 2:
                num = active[f'A{27}'].value
                name = active[f'B{27}'].value
                cabinet = active[f'C{27}'].value
                teacher = active[f'D{27}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 3:
                num = active[f'A{36}'].value
                name = active[f'B{36}'].value
                cabinet = active[f'C{36}'].value
                teacher = active[f'D{36}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 4:
                num = active[f'A{45}'].value
                name = active[f'B{45}'].value
                cabinet = active[f'C{45}'].value
                teacher = active[f'D{45}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson


def send_day_sixth(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_six(clas)
    send_lesson(lesson, chat_id)


def get_day_seven(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{9}'].value
            name = active[f'B{9}'].value
            cabinet = active[f'C{9}'].value
            teacher = active[f'D{9}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 1:
            num = active[f'A{19}'].value
            name = active[f'B{19}'].value
            cabinet = active[f'C{19}'].value
            teacher = active[f'D{19}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 2:
            num = active[f'A{28}'].value
            name = active[f'B{28}'].value
            cabinet = active[f'C{28}'].value
            teacher = active[f'D{28}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 3:
            num = active[f'A{37}'].value
            name = active[f'B{37}'].value
            cabinet = active[f'C{37}'].value
            teacher = active[f'D{37}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif wd == 4:
            num = active[f'A{46}'].value
            name = active[f'B{46}'].value
            cabinet = active[f'C{46}'].value
            teacher = active[f'D{46}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
        elif clas == "10И":
            dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
            active = dataframe.active
            lesson = []
            if wd == 0:
                num = active[f'A{9}'].value
                name = active[f'B{9}'].value
                cabinet = active[f'C{9}'].value
                teacher = active[f'D{9}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 1:
                num = active[f'A{18}'].value
                name = active[f'B{18}'].value
                cabinet = active[f'C{18}'].value
                teacher = active[f'D{18}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 2:
                num = active[f'A{28}'].value
                name = active[f'B{28}'].value
                cabinet = active[f'C{28}'].value
                teacher = active[f'D{28}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 3:
                num = active[f'A{37}'].value
                name = active[f'B{37}'].value
                cabinet = active[f'C{37}'].value
                teacher = active[f'D{37}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson
            elif wd == 4:
                num = active[f'A{46}'].value
                name = active[f'B{46}'].value
                cabinet = active[f'C{46}'].value
                teacher = active[f'D{46}'].value
                lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
                return lesson


def send_day_seventh(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_seven(clas)
    send_lesson(lesson, chat_id)


def get_day_eight(clas):
    wd = datetime.datetime.today().weekday()
    if clas == "10Т":
        dataframe = openpyxl.load_workbook("Расписание 10Т.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 0:
            num = active[f'A{10}'].value
            name = active[f'B{10}'].value
            cabinet = active[f'C{10}'].value
            teacher = active[f'D{10}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson
    elif clas == "10И":
        dataframe = openpyxl.load_workbook("Расписание 10И.xlsx")
        active = dataframe.active
        lesson = []
        if wd == 1:
            num = active[f'A{19}'].value
            name = active[f'B{19}'].value
            cabinet = active[f'C{19}'].value
            teacher = active[f'D{19}'].value
            lesson.append(f'{num}. {name}, каб. {cabinet}, учитель: {teacher}')
            return lesson


def send_day_eighth(chat_id):
    print(chat_id)
    clas = get_user_class(chat_id)
    lesson = get_day_eight(clas)
    send_lesson(lesson, chat_id)


def send_lesson(lesson, chat_id):
    bot.send_message(chat_id, lesson)


def run_bot():
    bot.polling(none_stop=True)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    import threading

    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_schedule).start()
