import datetime
import telebot
import sqlite3


conn = sqlite3.connect('salon.db', check_same_thread=False)
cur = conn.cursor()

print("База данных создана и успешно подключена к SQLite")
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

def descrip(k):# переводим время

    if k < 20:
        res="1"+str(k//2)
    else :
        res = "2" + str((k-20) // 2)
    if k%2==0:
        res+=":00"
    else:
        res += ":30"
    return res

def cript(s): # из времени в число
    k= int(s[1])*2
    if s[3]=='3' :
        k+=1
    return k


def shed(s, count):
    #время процедурв еще надо - count
    ar=[]
    sr = s.split(",")#делим по промежуткам
    for i in sr:
        # если в i нет -
        if i.find("-") != -1:
            k = i.split("-")
            begin = int(k[0])
            end = int(k[1])
            for j in range(begin,end-count+1):# вычитаем время, которе займет процедура
                ar.append(descrip(j))

    return ar




class Keyboard:
    def __init__(self, bot):
        self.bot = bot

    def list_of_times(self):
        return shed("0-24", 1)

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
        q = "UPDATE master SET rating = {}, countClient = {} WHERE id =  {}".format(str(newRt), str(count + 1), str(id))
        executeQuery(q)

    def reminder_to_vote_dict(self):  # напоминание оценить мастера
        dict_of_answ={}
        q = "SELECT idUser, idMaster, lastname, name FROM record join master on(idMaster=id)  WHERE  strftime('%d',idDay) - strftime('%d',datetime('now')) = 0"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            dict_of_answ[row[0]]=[row[1],row[2], row[3]]
        return dict_of_answ


    def kb_reminder(self):  # напоминание об услуге
        dict_of_answ={}
        q = "SELECT idUser, name, record.time FROM record join service on (idService=id) WHERE strftime('%d',idDay) - strftime('%d',datetime('now')) = 1;"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            dict_of_answ[row[0]]=[row[1],row[2]]
        for id in dict_of_answ.keys():
            print(id,dict_of_answ[id][0],dict_of_answ[id][1] )
            self.bot.send_message(chat_id=id,text="Здравствуйте!  Напоминаем, что у вас завтра {} в {}".format(dict_of_answ[id][0],descrip(int(dict_of_answ[id][1]))))

    def display_time_of_master(self, id_of_client, master, procedure,date):#ыводим режим работы мастера в определнный день
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        date = "'{}'".format(date)
        proc = "'{}'".format(procedure)
        fname = "'{}'".format(master.split(' ')[1]).replace('(Топ)','')
        lname = "'{}'".format(master.split(' ')[0])

        # print(date, proc, fname, lname)

        # находим время процедуры
        q = "select time from service where name=" + proc
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            print(row[0])
            res1 = row[0]

        # Находим id Мастера
        q = "select id from master where name=" + fname + " and lastname=" + lname
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            print(row[0])
            res2 = row[0]

        # основной запрос
        q = "Select freeTime from calendar where (SELECT strftime('%s',idDay) - strftime('%s',  +" +date + "))=0 and idMaster=" + str(res2)

        executeQuery(q)
        result = cur.fetchall()

        if result == []:# если мастер в этот день не работает
            text_choose = 'К сожалению, мастер в этот день '+date+' не работает'

        else:
            for row in result:
                print(row[0])
                s = row[0]

            # выводит массив свободного времени
            ar = shed(s, res1)
            for i in range(0, len(ar), 3):
                if i + 1 == len(ar):
                    markup.row(ar[i])
                elif i + 2 == len(ar):
                    markup.row(ar[i], ar[i + 1])
                else:
                    markup.row(ar[i], ar[i + 1], ar[i + 2])

            text_choose = 'Выберите время: '

        self.bot.send_message(chat_id= id_of_client,
                              text=text_choose,
                              reply_markup=markup)

    def display_time_of_all_masters(self,call, procedure,date):#ыводим режим работы мастера в определнный день
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        date = "'{}'".format(date)
        proc = "'{}'".format(procedure)

        # print(date, proc)
        # находим время процедуры
        q = "select time from service where name=" + proc
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            res1 = row[0]

        # Находим id Мастеров
        q = "select id from master where service like '%"+procedure+"%';"
        res2 ="("
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            res2 += str(row[0])+","
        res2 = res2[:-1] +')'
        print("res2", res2)

        q = "Select idMaster from calendar where (SELECT strftime('%s',idDay) - strftime('%s',  +" +date + "))=0 and idMaster in "+res2 +";"
        executeQuery(q)
        result = cur.fetchall()

        if result == []:# если мастера в этот день не работает
            text_all_masters_shed = 'К сожалению, выбранные мастера в этот день '+date+' не работают'

        else:
            ids = []
            for row in result:
                print(row[0])
                ids.append(row[0])
            text_all_masters_shed = "В этот день работают следюущие мастера:\n"
            for id in ids:
                q = "Select * from master where  id =" + str(id) + ";"
                executeQuery(q)
                i = cur.fetchall()
                print(i)
                text_all_masters_shed += '{} {}{}  рейтинг: {}\n'.format(i[0][1], i[0][2], top(i[0][4]), i[0][5])
                markup.row(('{} {}{}  рейтинг: {}'.format(i[0][1], i[0][2], top(i[0][4]), i[0][5])))
                q = "Select freeTime from calendar where (SELECT strftime('%s',idDay) - strftime('%s',  +" + date + "))=0 and idMaster=" + str(
                    id)
                executeQuery(q)
                result = cur.fetchall()
                for row in result:
                    print(row[0])
                    s = row[0]
                # выводит массив свободного времени
                ar = shed(s, res1)

                for i in ar:
                    text_all_masters_shed += str(i) + '\n'



        markup.row('Вернуться на главную')
        self.bot.send_message(chat_id=call.message.chat.id,
                                  text=text_all_masters_shed,
                                  reply_markup=markup)


    def insert_record(self,message, master, procedure,dates, time):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')

        date = "'{}'".format(dates)
        proc = "'{}'".format(procedure)
        fname = "'{}'".format(master.split(' ')[1]).replace('(Топ)', '')#имя
        lname = "'{}'".format(master.split(' ')[0])#Фамилия
        print(date, proc, fname, lname)
        timeuncode= cript(time) #нужно раскодировать
        #Нужен запрос на запись
        # находим время процедуры
        q = "select id, time from service where name= '" + procedure+"'"
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            print(row[0])
            res1 = row[1]
            idproc =row[0]

        # Находим id Мастера
        q = "select id from master where name=" + fname + " and lastname=" + lname
        executeQuery(q)
        result = cur.fetchall()
        for row in result:
            print(row[0])
            res2 = row[0]

        # основной запрос
        q = "Select freeTime from calendar where (SELECT strftime('%s',idDay) - strftime('%s',  +" + date + "))=0 and idMaster=" + str(res2)

        executeQuery(q)
        result = cur.fetchall()

        for row in result:
            print(row[0])
            s = row[0]

        res3 =""
        sr = s.split(",")  # делим по промежуткам
        for i in sr:
            # если в i нет -
            if (i != "") and (i.find("-") != -1):
                k = i.split("-")
                print("k ", k)
                begin = int(k[0])
                end = int(k[1])

                if res1 < (end - begin + 1):  # если процедура не занимает все свободное время или хватит вообще времени
                    if begin <= timeuncode < end:
                        if begin == timeuncode:
                            res3 += str(timeuncode) + '-' + k[1] + ','
                        elif timeuncode == end - res1 + 1:
                            res3 += k[0] + '-' + str(timeuncode) + ','
                        else:  # если выбрал время в середине
                            res3 += k[0] + '-' + str(timeuncode) + ',' + str((timeuncode + res1)) + '-' + k[1] + ','
                    else:  # если выбранное время не попадает в наш промежуток, записываем его без изменений
                        res3 += i + ','

            elif (i != "") and (i.find("-") == -1):# если одно чило без -
                res3+=i+','

            #168671681,1,1,'15','2021-12-07 00:00:00'      idUser, idMaster, idService, time,idDay

        print(dates)
        datet =str(dates)+" 00:00:00'"
        print(datet)

        q = "INSERT into record VALUES ("+ str(message.from_user.id)+","+str(res2)+"," + str(idproc) +",'"+str(timeuncode)+"','"+ datet+");"
        print(q)
        executeQuery(q)

        q = "UPDATE calendar SET freeTime='" + res3 + "' WHERE idMaster=" + str(res2) + " and idDay='" + datet
        executeQuery(q)

        text_about_record = "Вы записались на {} в {} на {}".format(procedure, time, dates.strftime('%d.%m.%y'))
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_about_record,
                              reply_markup=markup)