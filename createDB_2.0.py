import pymysql
from pymysql import connect
# from mysql.connector import connect, Error
import datetime as dt
class workWithDataBase():
    def __init__(self):
        self.conn = connect(host='localhost',
                       user='root',
                       password='root')
        self.cur = self.conn.cursor()

    def executeQuery(self, str):
        self.cur.execute(str)
        self.conn.commit()

    def createDB(self, nameDB):
        query = "CREATE DATABASE IF NOT EXISTS `{}`".format(nameDB)
        self.executeQuery(query)

    def connectDB(self, nameDB):
        self.conn = connect(host='localhost',
                       user='root',
                       password='root',
                       database=nameDB)
        self.cur = self.conn.cursor()

    def insertMaster(self, lastN, firstN, prof, istop, rating, count):
        q = "INSERT INTO master (lastName, firstName, profession, isTop, rating, countClient)" \
                "VALUES (\"{}\", \"{}\",\"{}\", {}, {}, {})".format(lastN, firstN, prof, istop, rating, count)
        self.executeQuery(q)

    def insertService(self, name, time, priceTop, price, profession):
        q = "INSERT INTO service (serviceName, serviceTime, priceTop, price)" \
            "VALUES (\"{}\", \"{}\", {}, {})".format(name, time, priceTop, price)
        self.executeQuery(q)
        # получаем id вставленной услуги
        servId = self.cur.lastrowid
        # получаем id мастеров для данной услуги
        q = "SELECT id FROM master WHERE profession = \"{}\"".format(profession)
        self.executeQuery(q)
        result = self.cur.fetchall()
        # прописываем связь мастеров и новой услуги
        for row in result:
            print(row[0])
            q = "INSERT INTO master_service (masterId, serviceID) VALUES ({}, {})".format(row[0],servId)
            print(q)
            self.executeQuery(q)

    def insertMasterWorkDayAuto(self, masterId, start,end, work, weekend):
        date = start - dt.timedelta(1)
        while(date<end):
            for n in range(work):
                if(date<end):
                    date = date + dt.timedelta(1)
                    q = "INSERT INTO master_working_day(masterId, workingDay)" \
                        " VALUES (\"{}\", \"{}\")".format(masterId,date.date())
                    self.executeQuery(q)
                else:
                    break
            for n in range(1, weekend+1):
                if (date < end):
                    date = date + dt.timedelta(1)
                else:
                    break
    def insertMasterWorkDay(self, masterId, date):
        q = "INSERT INTO master_working_day(masterId, workingDay)" \
            " VALUES (\"{}\", \"{}\")".format(masterId, date.date())
        self.executeQuery(q)

    def insertCalendar(self, timeStart, timeEnd, dayStart, dayEnd):
        dayDict = {1:'Пн', 2:'Вт', 3:'Ср',4:'Чт',
                   5:'Пт',6:'Сб',7:'Вск'}
        step = int(divmod((timeEnd - timeStart).total_seconds(), 1800)[0])

        for d in range(dayStart, dayEnd+1):
            time = timeStart - dt.timedelta(minutes=30)
            for n in range(step):
                if (time < timeEnd):
                    time = time + dt.timedelta(minutes=30)
                    q = "INSERT INTO calendar(dayId, dayName, timeName) " \
                        "VALUES ({}, \"{}\", \"{}\")".format(d, dayDict[d],time.time())
                    self.executeQuery(q)
                else:
                    break
    def updateRating(self,idClient, ass):
        q ="SELECT masterId from record " \
           "where clientId = {} and dateRecord = \"2021-12-06\"-- CURDATE() " \
           "group by masterId".format(idClient)                                    # ПОМЕНЯТЬ НА CURDATE()!!!!!!!!
        self.executeQuery(q)
        result = self.cur.fetchall()
        for row in result:
            q = "Select rating, countClient from master " \
                "WHERE id = {}".format(row[0])
            self.executeQuery(q)
            rt = 0; count = 0
            result = self.cur.fetchall()
            for row in result:
                rt = row[0]
                count = row[1]
            newRt = (rt*count + ass)/(count+1)
            q = "UPDATE master SET rating = {}, countClient = {} " \
                "WHERE id = {}".format(newRt, count+1, row[0])
            self.executeQuery(q)

    def createDBwith0(self):
        '''скрипт для создании бд с нуля'''
        # создаем бд
        self.createDB("dbbeautysalon_2")
        # создадим таблицу мастер
        query = "CREATE TABLE master(" \
                "id INT AUTO_INCREMENT," \
                "lastname VARCHAR(20)," \
                "firstname VARCHAR(20)," \
                "profession VARCHAR(20)," \
                "isTop BOOL," \
                "rating DOUBLE," \
                "countClient int," \
                "CONSTRAINT PK_master PRIMARY KEY(id))"
        self.executeQuery(query)

        # создадим таблицу услуги
        query = "CREATE TABLE service(" \
                "id INT AUTO_INCREMENT," \
                "serviceName VARCHAR(100)," \
                "serviceTime TIME," \
                "priceTop INT," \
                "price INT," \
                "CONSTRAINT PK_service PRIMARY KEY (id))"
        self.executeQuery(query)

        # создадим таблицу соспоставления мастера и услуг
        query = "CREATE TABLE master_service(" \
                "id          INT AUTO_INCREMENT," \
                "masterId    INT," \
                "serviceId   INT," \
                "CONSTRAINT PK_mast_Serv PRIMARY KEY (id)," \
                "CONSTRAINT FOREIGN KEY (masterId) REFERENCES master(id)," \
                "CONSTRAINT FOREIGN KEY (serviceId) REFERENCES service(id))"
        self.executeQuery(query)

        # создадим таблицу Календарь. Хранит id дня недели (1-7), название дня и время
        query = "CREATE TABLE calendar(" \
                "id         INT AUTO_INCREMENT," \
                "dayId     	INT," \
                "dayName    VARCHAR(20)," \
                "timeName	TIME," \
                "CONSTRAINT PK_calendar PRIMARY KEY (id))"
        self.executeQuery(query)

        # создадим таблицу Запись, хранит id клиента, мастера, услуги, дату записи, время начала и окончания процедуры
        query = "CREATE TABLE record(" \
                "id         INT AUTO_INCREMENT," \
                "clientId	INT," \
                "masterId   INT," \
                "serviceId	INT," \
                "dateRecord	DATE," \
                "timeStart	TIME," \
                "timeEnd	TIME," \
                "CONSTRAINT PK_record PRIMARY KEY (id)," \
                "CONSTRAINT FOREIGN KEY(masterId) REFERENCES master(id)," \
                "CONSTRAINT FOREIGN KEY(serviceId) REFERENCES service(id))"
        self.executeQuery(query)

        #создадим таблицу рабочих дней, хранит id мастера и дату, когда он работает
        query = "CREATE TABLE master_working_day(" \
                "id 		 INT AUTO_INCREMENT," \
                "masterId    INT," \
                "workingDay  DATE," \
                "CONSTRAINT PK_mastwork PRIMARY KEY (id)," \
                "CONSTRAINT UNIQUE (masterId,workingDay)," \
                "CONSTRAINT FOREIGN KEY (masterId) REFERENCES master(id))"
        self.executeQuery(query)

        # Автозаполнение рабочих дней: id мастера, даты начала и конца заполнения, график работы (5/2, 2/2 и тп)
        # можно делать раз в месяц
        for i in range(1,8): #первые 7 человек работают 5/2
            self.insertMasterWorkDayAuto(i, dt.datetime.strptime('2021-12-06', '%Y-%m-%d'),
                                  dt.datetime.strptime('2021-12-31', '%Y-%m-%d'), 5, 2)
        for i in range(8,15): #оставшиеся 7 человек работают 2/2
            self.insertMasterWorkDayAuto(i, dt.datetime.strptime('2021-12-06', '%Y-%m-%d'),
                                  dt.datetime.strptime('2021-12-31', '%Y-%m-%d'), 2, 2)

        # # заполнение рабочих дней на конкретную дату: id мастера, дата рабочего дня
        # self.insertMasterWorkDay(2, dt.datetime.strptime('2021-12-06', '%Y-%m-%d'))

        # заполенение календаря: время начала и конца работы, id дня начала и конца раб.недели
        # считается, что салон работает с 10 до 21 каждый день недели
        self.insertCalendar(dt.datetime.strptime('10:00', '%H:%M'), dt.datetime.strptime('21:00', '%H:%M'), 1,7)

    def exampleQuery(self):
        '''скрипт простых запросов(ненужных, тк бд заполняется не в python)'''
        self.insertMaster("Растремина", "Анастасия", "ногтевой сервис", False, 4.5, 10)
        # добавление новой услуги, в конце профессия/сфера мастера для связи новой услуги с нужными мастерами
        self.insertService("маникюр","1:30", 2000, 1000, "ногтевой сервис")



if __name__ == '__main__':
    db = workWithDataBase()
    #подключаемся к нашей бд
    db.connectDB("dbbeautysalon_2")

    # query = "DROP TABLE IF EXISTS master, service, calendar, record, master_working_day, master_service"
    # db.executeQuery(query)

    # Перечень услуг, цен
    q = "Select serviceName, serviceTime, price,priceTop from service"
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        time = dt.datetime.strptime(str(row[1]), '%H:%M:%S').strftime('%H:%M')
        print("{} {}ч. {}руб ({}руб)".format(row[0], time, row[2], row[3]))

    # ЗАПИСАТЬСЯ НА ПРОЦЕДУРУ: даем перечень услуг и просим ответить id-ком услуги
    q = "Select id, serviceName, serviceTime from service"
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        print("{}. {}".format(row[0], row[1]))
    # получили id услуги, запоминаем время процедуры в минутах
    idServ = 4
    timeServ = int(divmod(result[idServ-1][2].total_seconds(), 60)[0])
    # спрашиваем нужен конкретный мастер или любой?
    # если конкретный мастер, то даем перечень мастеров и просим ответить id-ком мастера
    # мастеров в каждой сфере немного (максимум 4), можно кнопки сделать или просто списком вывести
    q = "select m.id, m.lastName, m.firstName, m.isTop, m.rating " \
        "from master_service ms " \
        "left join master m on m.id = ms.masterId " \
        "where serviceId = {}".format(idServ)
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        top = 'Топ-мастер' if row[3] else ''
        print("{}. {} {} - {} рейтинг {}".format(row[0], row[1],row[2],top,row[4]))
    # узнали id мастера из ответа
    idMast = 13
    # даем перечень свободных окон на запись для данного мастера с учетом длительности процедуры
    q = "select dayName, workingDay, timeName " \
        "from master m " \
        "left join master_working_day mwd " \
        "on m.id = mwd.masterId and workingDay<=DATE_ADD(CURDATE(), INTERVAL 7 day) " \
        "left join calendar c on c.dayId = WEEKDAY(workingDay)+1 " \
        "left join (select masterId, dateRecord, timeStart, timeEnd from record " \
        "			where dateRecord >=CURDATE()) r " \
        "on c.dayId = WEEKDAY(dateRecord)+1 and m.id = r.masterId " \
        "	and ((timeStart <= timeName and timeName< timeEnd) or " \
        "		(timeName < timeStart and DATE_ADD(timeName, INTERVAL {} minute) > timeStart) ) " \
        "where dateRecord is null and DATE_ADD(timeName, INTERVAL {} minute) <=\"21:00\" " \
        "	  and m.id = {}".format(timeServ, timeServ, idMast)
    db.executeQuery(q)
    result = db.cur.fetchall()
    i = 1
    for row in result:
        time = dt.datetime.strptime(str(row[2]), '%H:%M:%S').strftime('%H:%M')
        print("{}. {}({}) - {}".format(i, row[0], row[1], time))
        i+=1

    # просим ответить id-ком удобного времени, записываем в переменные: дату, время начала и конца процедуры
    idRec = 4
    dateRec = result[idRec-1][1]
    timeStartRec = dt.datetime.strptime(str(result[idRec-1][2]), '%H:%M:%S')
    timeEndRec = timeStartRec + dt.timedelta(minutes=timeServ)
    # записываем в таблицу record
    idClient = 101
    q = "INSERT INTO record (clientId, masterId, sericeId, dateRecord, timeStart, timeEnd) " \
        "VALUES ( {}, {}, {}, \"{}\", \"{}\", \"{}\")".\
        format(idClient, idMast, idServ, dateRec, timeStartRec.strftime('%H:%M'), timeEndRec.strftime('%H:%M'))
    # db.executeQuery(q)
    print("Записали Вас на {} в {}".format(dateRec, timeStartRec.strftime('%H:%M')))
    # Запись сделана

    # если мастер любой, то получаем свободные записи для всех мастеров, способных предоставить данную услугу
    q = "select m.id, lastName, firstName, dayName, workingDay, timeName " \
        "from master m " \
        "left join master_working_day mwd " \
        "on m.id = mwd.masterId and workingDay<=DATE_ADD(CURDATE(), INTERVAL 7 day) " \
        "left join calendar c on c.dayId = WEEKDAY(workingDay)+1 " \
        "left join (select masterId, dateRecord, timeStart, timeEnd from record " \
        "			where dateRecord >=CURDATE()) r " \
        "on c.dayId = WEEKDAY(dateRecord)+1 and m.id = r.masterId " \
        "	and ((timeStart <= timeName and timeName< timeEnd) or " \
        "		(timeName < timeStart and DATE_ADD(timeName, INTERVAL {} minute) > timeStart) )" \
        "where dateRecord is null and DATE_ADD(timeName, INTERVAL {} minute) <=\"21:00\"" \
        "	  and m.id in (SELECT m.id FROM master m" \
        "				   left join master_service ms on ms.masterId = m.id" \
        "					where serviceId = {})" \
        "order by m.id".format(timeServ, timeServ, idServ)
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        time = dt.datetime.strptime(str(row[5]), '%H:%M:%S').strftime('%H:%M')
        print("{}. {} {}: {}({}) - {}".format(i, row[1], row[2], row[3], row[4],time))
        i += 1
    # получаем в ответ id-ник удобного времени
    idRec2 = 15
    idMast2= result[idRec2-1][0]
    dateRec = result[idRec2-1][4]
    timeStartRec = dt.datetime.strptime(str(result[idRec-1][5]), '%H:%M:%S')
    timeEndRec = timeStartRec + dt.timedelta(minutes=timeServ)
    # дальше запись скрипт был выше

    # ЗАПИСАТЬСЯ К МАСТЕРУ: даем перечень мастеров
    # ЛИБО всех сразу выводим (но на данный момент их 14):
    q = "select id, lastName, firstName, isTop, rating from master"
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        top = 'Топ-мастер' if row[3] else ''
        print("{}. {} {} - {} рейтинг {}".format(row[0], row[1], row[2], top, row[4]))
    # ЛИБО предлагаем выбрать сначала "профессию"( ногтевой сервис, визажист, парикмахер, массажист и тд)
    # можно списоком/кнопками
    q = "SELECT profession FROM master group by profession"
    db.executeQuery(q)
    result = db.cur.fetchall()
    i=1
    for row in result:
        print("{}. {}".format(i,row[0]))
        i+=1
    # в ответ получаем id профессии и затем выводим мастеров
    idProf = 3
    nameProf = result[idProf-1][0]
    q = "select id, lastName, firstName, isTop, rating from master where profession = \"{}\"".format(nameProf)
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        top = 'Топ-мастер' if row[3] else ''
        print("{}. {} {} - {} рейтинг {}".format(row[0], row[1], row[2], top, row[4]))

    # получаем id мастера, а дальше вывод своб.окон как в варианте ПРОЦЕДУРА->КОНКР.МАСТЕР->ЗАПИСЬ

    # напоминалки клиентам на завтра
    # выбираем id клиента, ФИ мастера, название услуги, время записи
    q = "select clientId, lastName, firstName, serviceName, timeStart " \
        "from record r " \
        "left join master m on m.id = r.masterId " \
        "left join service s on s.id = r.serviceId " \
        "where dateRecord = DATE_ADD(\"2021-12-05\", INTERVAL 1 day)"        # ПОМЕНЯТЬ НА CURDATE()!!!!!!!!
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        row[0]  # id-ник клиента
        time = dt.datetime.strptime(str(row[4]), '%H:%M:%S').strftime('%H:%M')
        print("Здравствуйте! Напоминаем, что завтра Вы записаны к мастеру {} {} "
              "на процедуру \"{}\" в {}".
              format(row[1], row[2], row[3], time))

    # просьба оценить процедуру
    # выбираем id клиента, у к-х была сегодня запись
    q = "select clientId, masterId from record " \
        "where dateRecord = \"2021-12-06\"-- CURDATE()"                 # ПОМЕНЯТЬ НА CURDATE()!!!!!!!!
    db.executeQuery(q)
    result = db.cur.fetchall()
    for row in result:
        row[0] #id-ник клиента
        print("Добрый вечер! Оцените, пожалуйста работу мастера от 1 до 5")

    # id мастера не знаем, находим его по дате процедуры и id клиента, затем обновляем рейтинг и кол-во клиентов
    idClient2= 101
    # db.updateRating(idClient2, 5)



