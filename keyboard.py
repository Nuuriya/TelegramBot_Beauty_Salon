import datetime
import telebot
from pymysql import connect
from pymysql import connect
# from mysql.connector import connect, Error
import datetime


text_about = '''
Что-то очень инетересное по Python
Сcылки на что-то
'''

text_start = '''
Здравствуйте! Вас приветствует бот
салона красоты "Из уродки в красотку".
Чем могу помочь?
'''
text_promo = '''
Сейчас в нашем салоне действуют следющие акции:\n
1. Маникюр на каждый 11 палец - БЕСПЛАТНО!\n
2.\n
3.\n
4.\n
'''
text_services = '''
Услуга         Цена(мастер)    Цена(Топ мастер)   Время\n
'''
conn = connect(host='localhost',
                           user='root',
                           password='87654W!',
                           database='dbbeautysalon')
cur = conn.cursor()

def executeQuery(str):
    cur.execute(str)
    conn.commit()

def vremya(a):
    s=str(a//2)
    if a%2==0:
        s+=":00 час."
    else:
        s+=":30 час."
    return(s)

def top(a):
    if a==1:
        return "(Топ)"
    return ""

class Keyboard:
    def __init__(self, bot):
        self.bot = bot

    def display_start(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_start,
                              reply_markup=markup)
    def display_main(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        text_mess="Чем помочь?"
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_mess,
                              reply_markup=markup)
    def display_services(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть акции')
        #
        q = "Select * from service"
        executeQuery(q)
        results = cur.fetchall()
        #
        temp = text_services + "\n"
        for i in results:
            temp += (i[1] + "     " + str(i[2]) + "руб.            " + str(i[3]) + "руб.                     " + (
                vremya(i[4])) + "\n")

        self.bot.send_message(chat_id=message.from_user.id,
                              text=temp,
                              reply_markup=markup)
    def display_promo(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_promo,
                              reply_markup=markup)

    def display_procedures(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        q = "Select name from service"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            markup.row(row[0])
        markup.row('Вернуться на главную')
        text_procedures='Отлично! На какую процедуду хотите записаться?'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_procedures,
                              reply_markup=markup)

    def display_do_you_want_master(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Да')
        markup.row('Нет')
        markup.row('Выбрать процедуру')
        markup.row('Вернуться на главную')
        text_master='Хотите записаться к определенному мастеру?'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_master,
                              reply_markup=markup)
    def display_of_masters(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # я пока сама выбрала процедуру
        pr ="маникюр"
        q = "Select * from master where service like %"+pr+"%"
        executeQuery(q)
        result = cur.fetchall()
        for i in result:
            markup.row(('{} {}{}  рейтинг: {}'.format(i[1], i[2], top(i[4]), i[5])))
        markup.row('Выбрать процедуру')
        markup.row('Вернуться на главную')
        text_choose='Выберете мастера:'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_choose,
                              reply_markup=markup)

    def display_of_all_masters(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        q = "Select * from master"
        executeQuery(q)
        result = cur.fetchall()
        for i in result:
            markup.row(('{} {}{}  рейтинг: {}'.format(i[1],i[2],top(i[4]),i[5])))
        markup.row('Вернуться на главную')
        text_choose='Выберете мастера:\n'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_choose,
                              reply_markup=markup)
    def display_last(self, message, procedure,date):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        text_choose='Вы записаны на процедуру {} на {}. Ждем Вас!'.format(procedure, date)
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_choose,
                              reply_markup=markup)
    def display_vote(self, id, master):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('★','★★','★★★','★★★★','★★★★★')
        text_vote= 'Спасибо, что посетили Наш салон! Пожалуйста оцените нашего мастера {}'.format(master)
        self.bot.send_message(chat_id=id,
                              text=text_vote,
                              reply_markup=markup)
