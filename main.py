import time
import openpyxl
import telebot
from telebot import types
import json

bot = telebot.TeleBot('6897460981:AAFyclV4ixpEON5WuNNSyB1TSTNiv3IQ_R0')
lessons = []
users = []

try:
    with open('lessons.json', 'r', encoding='utf-8') as file:
        lessons = json.loads(file.read())

    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.loads(file.read())
except Exception as e:
    print(e)


def save_data():
    with open('lessons.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(lessons, ensure_ascii=False))
    with open('users.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(users, ensure_ascii=False))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    class_10t = types.KeyboardButton("10t")
    class_10i = types.KeyboardButton("10И")
    markup.add(class_10t, class_10i)
    m = bot.send_message(chat_id, 'Привет! В каком ты классе?', reply_markup=markup)
    bot.register_next_step_handler(m, know_user_class)


def know_user_class(message):
    chat_id = message.chat.id
    user_class = message.text
    if user_class == "10t" or user_class == "10И":
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
    bot.send_message(chat_id, 'Вот расписание для вас:')

    lesson = get_list_of_lessons("Monday")
    bot.send_message(chat_id, 'Расписание на понедельник:')
    send_lessons(lesson, chat_id)

    lesson = get_list_of_lessons("Tuesday")
    bot.send_message(chat_id, 'Расписание на вторник')
    send_lessons(lesson, chat_id)

    lesson = get_list_of_lessons("Wednesday")
    bot.send_message(chat_id, 'Расписание на среду')
    send_lessons(lesson, chat_id)

    lesson = get_list_of_lessons("Thursday")
    bot.send_message(chat_id, 'Расписание на четверг')
    send_lessons(lesson, chat_id)

    lesson = get_list_of_lessons("Friday")
    bot.send_message(chat_id, 'Расписание на пятницу')
    send_lessons(lesson, chat_id)


def send_lessons(lesson, chat_id):
    for i in range(len(lesson)):
        bot.send_message(chat_id, lesson[i])
        time.sleep(1)

def get_list_of_lessons(day):
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




bot.polling()
