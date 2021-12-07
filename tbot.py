from datetime import date

import telebot
import schedule
from threading import Thread
from time import sleep
from keyboard import Keyboard
import telegramcalendar as tgc


# ваш токен
TOKEN = '2102340203:AAFs-2l-3z6UoCwvi1vatLIHxuziO7Bc-Ls'  # Нурия
#TOKEN = '2144374054:AAHi3LyZLWOv3cMfHMVhR7pCKKQeaeb7pbo'  # Диляра
bot = telebot.TeleBot(TOKEN)
keyboard = Keyboard(bot)
deadline_date = tgc.datetime.datetime.now()
list_of_times=keyboard.list_of_times()#список времени
list_of_procedure =  keyboard.list_of_procedures()#список процедур
global need_master
need_master=True
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

@bot.message_handler(func=lambda msg: msg.text == 'Записаться на процедуру' or msg.text == 'Выбрать процедуру', content_types=['text'])
def procedures(message):
    keyboard.display_procedures(message)


@bot.message_handler(func=lambda msg: msg.text in list_of_procedure, content_types=['text'])
def do_you_want_master(message):
    global procedure
    procedure = message.text#запомним процедуру на которую хочет записаться
    print(procedure)
    keyboard.display_do_you_want_master(message)

@bot.message_handler(func=lambda msg: msg.text == 'Да', content_types=['text'])
def do_you_want_master(message):
    global procedure
    print(procedure)
    keyboard.display_of_masters(message, procedure)

@bot.message_handler(func=lambda msg: msg.text == 'Нет' or (msg.text in keyboard.list_of_masters() and need_master==True), content_types=['text'])
#если клиент не хочет мастера пишет "нет", иначе он выбирает мастера из списка мастер будет в keyboard.list_of_masters(),
#если выбран мастер его нужно будет запомнить
def calendar(message):
    now = tgc.datetime.datetime.now()  # Текущая дата
    markup = tgc.create_calendar(now.year, now.month)
    global need_master
    if message.text!='Нет':
        global master
        master = message.text.split("  ")[0]  # запомним мастера к которому хочет записаться
        need_master = True
    else:
        need_master = False

    bot.send_message(message.from_user.id, "Пожалуйста, выберите дату: ",
                     reply_markup=markup)

#как можно сделать: написать запрос на проверку свободного времени, если оно есть, записываем клиента и выводим сообщение что записали
#иначе не записываем посылаем сообщение чтоб выбрал другой день и снова выводим календарь
#можно в сообщении до этого написать о свободных датах хз

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
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        ret_data = tgc.datetime.date(int(year), int(month), int(day))
        gg = ret_data.year
        mm = ret_data.month
        dd = ret_data.day
        global procedure
        global deadline_date
        deadline_date = date(gg, mm, dd)
        bot.edit_message_text(text=call.message.text+deadline_date.strftime('%d.%m.%y'),
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        global need_master
        if need_master:
            global master
            print(master, procedure)
            keyboard.display_time_of_master(call.message.chat.id, master, procedure,  deadline_date)
        else:
            keyboard.display_time_of_all_masters(call, procedure, deadline_date)
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

@bot.message_handler(func=lambda msg:  msg.text in keyboard.list_of_masters() and need_master==False, content_types=['text'])
#если клиент не хочет мастера пишет "нет", иначе он выбирает мастера из списка мастер будет в keyboard.list_of_masters(),
#если выбран мастер его нужно будет запомнить
def time_of_master(message):
    global master
    master = message.text.split("  ")[0]  # запомним мастера к которому хочет записаться
    global procedure
    global deadline_date
    keyboard.display_time_of_master(message.from_user.id, master, procedure, deadline_date)

@bot.message_handler(func=lambda msg: msg.text in list_of_times, content_types=['text'])
def write_to_db(message):
    global time
    time=message.text
    global deadline_date
    keyboard.insert_record(message, master, procedure,deadline_date, time)

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def reminder():#напоминание о процедуре
    keyboard.kb_reminder()

def vote():#напоминание оценить мастера
    dict_of_answ = keyboard.reminder_to_vote_dict()
    for id in dict_of_answ.keys():
        lastname = dict_of_answ[id][1]
        name = dict_of_answ[id][2]
        master = dict_of_answ[id][0]
        markup=keyboard.vote_keyboard(master)
        text_vote = 'Спасибо, что посетили Наш салон! Пожалуйста, оцените нашего мастера {} {}'.format(lastname, name)
        bot.send_message(chat_id=id,
                              text=text_vote,
                              reply_markup=markup)

@bot.callback_query_handler(func=lambda call: keyboard.separate_callback_data(call.data)[0] in
                                              ['1', '2', '3', '4', '5'])
def update_rating(call):
    (rate, id) = keyboard.separate_callback_data(call.data)
    print(rate, id)
    bot.edit_message_text(text="Спасибо за Ваш голос!",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id)
    keyboard.updateRating(int(id), int(rate))

if __name__ == "__main__":
    # Create the job in schedule.

    schedule.every().day.at("10:00").do(reminder)
    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.

    # scheduler()
    schedule.every().day.at("22:00").do(vote)
    Thread(target=schedule_checker).start()

    # And then of course, start your server.
    bot.polling()
