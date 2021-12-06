import datetime
import telebot
from pymysql import connect
from pymysql import connect
# from mysql.connector import connect, Error
import datetime


# conn = connect(host='localhost',
#                            user='root',
#                            password='87654W!',
#                            database='dbbeautysalon')
# бд нурии
conn = connect(host='localhost',
                           user='root',
                           database='dbbeautysalon')

cur = conn.cursor()
text_start = '''
Здравствуйте! Вас приветствует бот
салона красоты "Красотка".
Чем могу помочь?
'''
text_promo = '''
Сейчас в нашем салоне действуют следющие акции:\n
1. Маникюр на каждый 11 палец - БЕСПЛАТНО!\n
2. Приведи 3 подруги и получи скидку 20% на любую процедуру! \n
3. Назови секретное слово ТЕЛЕГРАМБОТ и получи скидку 5% на любую процедуру!\n
'''
text_services = '''
Услуга         Цена(мастер)    Цена(Топ мастер)   Время\n
'''




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

    def list_of_procedures(self):
        list=[]
        q = "Select name from service"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
           list.append(row[0])
        return list

    def list_of_masters(self):
        list=[]
        q = "Select * from master"
        executeQuery(q)
        result = cur.fetchall()
        for i in result:
            list.append('{} {}{}  рейтинг: {}'.format(i[1], i[2], top(i[4]), i[5]))
        return list

    def display_start(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        # markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_start,
                              reply_markup=markup)
    def display_main(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        # markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        text_mess="Чем помочь?"
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_mess,
                              reply_markup=markup)
    def display_services(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        # markup.row('Записаться к мастеру')
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
        # markup.row('Записаться к мастеру')
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
    def display_of_masters(self, message, procedure):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        pr=procedure
        q = "Select * from master where service like '%"+pr+"%';"
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

    def separate_callback_data(self, data):
        """ Separate the callback data"""
        return data.split(";")
    def vote_keyboard(self, master):
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('★', callback_data="1;{}".format(master))
        markup.row(btn1)
        btn2 = telebot.types.InlineKeyboardButton('★★', callback_data="2;{}".format(master))
        markup.row(btn2)
        btn3 = telebot.types.InlineKeyboardButton('★★★', callback_data="3;{}".format(master))
        markup.row(btn3)
        btn4 = telebot.types.InlineKeyboardButton('★★★★', callback_data="4;{}".format(master))
        markup.row(btn4)
        btn5 = telebot.types.InlineKeyboardButton('★★★★★', callback_data="5;{}".format(master))
        markup.row(btn5)
        return markup

    def updateRating(self, id, ass):
        q = "Select rating, countClient from master " \
            "WHERE id = %i" %id
        executeQuery(q)
        rt = 0
        count = 0
        result = cur.fetchall()
        for row in result:
            rt = row[0]
            count = row[1]
        newRt = (rt * count + ass) / (count + 1)
        q = "UPDATE master SET rating = %i, countClient = %i " \
            "WHERE id = %i" % (newRt, count + 1, id)
        executeQuery(q)

    def reminder_to_vote_dict(self):  # напоминание оценить мастера
        dict_of_answ={}
        q = "SELECT idUser, idMaster, lastname, name FROM record join master on(idMaster=id)  WHERE  date = CURRENT_DATE();"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            dict_of_answ[row[0]]=[row[1],row[2], row[3]]
        return dict_of_answ


    def kb_reminder(self):  # напоминание об услуге
        dict_of_answ={}
        q = "SELECT idUser, name, record.time FROM record join service on(idService=id) WHERE DATEDIFF(date, CURRENT_DATE()) = 1;"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            dict_of_answ[row[0]]=[row[1],row[2]]
        for id in dict_of_answ.keys():
            print(id,dict_of_answ[id][0],dict_of_answ[id][1] )
            self.bot.send_message(chat_id=id,text="Здравствуйте!  Напоминаем, что у вас завтра {} в {}".format(dict_of_answ[id][0],dict_of_answ[id][1]))

