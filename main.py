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
    schedule.every().day.at("15:13").do(send_notification, chat_id)


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
