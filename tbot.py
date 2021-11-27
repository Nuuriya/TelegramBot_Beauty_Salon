import telebot
import schedule
from threading import Thread
import asyncio
from time import sleep
from keyboard import Keyboard
import telegramcalendar as tgc

list_of_masters=['Маникюрова', 'Топ маникюрова','Педикюрова','топ Педикюрова','РЕсницева']
list_of_services = ['на маникюр', 'на педикюр','на наращивание ресниц','на эпиляцию']
# ваш токен
TOKEN = '2126834952:AAHnqsA1jtlibXDBVb_MENfJq4YI3PG6Fbs'  # Нурия
bot = telebot.TeleBot(TOKEN)
keyboard = Keyboard(bot)
deadline_date = tgc.datetime.datetime.now()

@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.from_user.id)
    keyboard.display_start(message)


@bot.message_handler(func=lambda msg: msg.text == 'Вернуться на главную', content_types=['text'])
def main(message):
    keyboard.display_main(message)


@bot.message_handler(func=lambda msg: msg.text == 'Посмотреть акции', content_types=['text'])
def promo(message):
    keyboard.display_promo(message)

@bot.message_handler(func=lambda msg: msg.text == 'Посмотреть услуги и цены', content_types=['text'])
def services(message):
    keyboard.display_services(message)

@bot.message_handler(func=lambda msg: msg.text == 'Записаться на процедуру', content_types=['text'])
def procedures(message):
    keyboard.display_procedures(message)

@bot.message_handler(func=lambda msg: msg.text == 'Записаться к мастеру', content_types=['text'])
def all_masters(message):
    keyboard.display_of_all_masters(message,list_of_masters)

@bot.message_handler(func=lambda msg: msg.text in list_of_services , content_types=['text'])
def do_you_want_master(message):
    keyboard.display_do_you_want_master(message)

@bot.message_handler(func=lambda msg: msg.text == 'Да', content_types=['text'])
def do_you_want_master(message):
    keyboard.display_of_all_masters(message,list_of_masters)

@bot.message_handler(func=lambda msg: msg.text == 'Нет', content_types=['text'])
def calendar(message):
    now = tgc.datetime.datetime.now()  # Текущая дата
    markup = tgc.create_calendar(now.year, now.month)
    bot.send_message(message.from_user.id, "Пожалуйста, выберите дату:",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: tgc.separate_callback_data(call.data)[0] in
                                              ['IGNORE', 'PREV-MONTH', 'NEXT-MONTH', 'DAY'])
def keyboard_input_text(call):
    (action, year, month, day) = tgc.separate_callback_data(call.data)
    curr = tgc.datetime.date(int(year), int(month), 1)
    if action == "IGNORE":
        # Продолжаем игнорить неюзабильные кнопки
        bot.answer_callback_query(callback_query_id=call.id)
    elif action == "DAY":
        # Выбран день
        # Cкрываем календарь (изменяем сообщение, не посылая markup)
        # Здесь можем написать выбранную дату и проверку "верно/нет"
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        ret_data = tgc.datetime.date(int(year), int(month), int(day))
        # bot.send_message(message.from_user.id, "Домашнее задание на " + ret, reply_markup=markup)
        gg = ret_data.year
        mm = ret_data.month
        dd = ret_data.day
        global deadline_date
        deadline_date = ret_data
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Да')
        markup.row('Нет')
        bot.send_message(call.message.chat.id, "Вы записались на {}.{}.{}".format(dd, mm, gg),
                         reply_markup=markup)
        # Важно запомнить дату
    elif action == "PREV-MONTH":
        pre = curr - tgc.datetime.timedelta(days=1)
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=tgc.create_calendar(int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + tgc.datetime.timedelta(days=31)
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=tgc.create_calendar(int(ne.year), int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="Something went wrong!")

some_id=168671681
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def reminder():#напоминание о процедуре
    bot.send_message(some_id, "Здравствуйте!  Напоминаем, что у вас завтра процедура в 11:00")

def vote():#напоминание оценить мастера
    id=some_id
    master="aaa"
    keyboard.display_vote(id, master)

async def scheduler():
    schedule.every().day.at("21:10").do(vote)
    #aioschedule.every(1).hours.do(start_function) каждый час
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
if __name__ == "__main__":
    # Create the job in schedule.
    # schedule.every().day.at("10:30").do(reminder)
    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.

    # scheduler()
    schedule.every().day.at("21:40").do(vote)
    Thread(target=schedule_checker).start()

    # And then of course, start your server.
    bot.polling()
