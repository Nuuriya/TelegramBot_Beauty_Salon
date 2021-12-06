import pymysql
from pymysql import connect
from datetime import datetime, date, time
# from mysql.connector import connect, Error
import datetime

def executeQuery(str):
    cur.execute(str)
    conn.commit()

def insertMaster(last, name, serv, istop, rating, count):
    q = "INSERT INTO master (lastname, name, service, isTop, rating, countClient)" \
            "VALUES (\"%s\", \"%s\",\"%s\", %s, %d, %i)" %(last, name, serv, istop, rating, count)
    print(q)
    executeQuery(q)
def insertService(name, priceTop, price, time):
    q = "INSERT INTO service (name, priceTop, price, time) " \
        "VALUES (\"%s\", %i, %i, %i)" % (name, priceTop, price, time)
    print(q)
    executeQuery(q)
def insertClient(idUser, idMaster, idService, time, idDay):
    q = "INSERT INTO record (idUser, idMaster, idService, time,  idDay)" \
            " VALUES ( %i, %i,  %i, \"%s\",  \"%s\")" % (idUser, idMaster, idService, time,idDay)
    print(q)
    executeQuery(q)
def insertCalendar(idDay,idMaster, freeTime):
    q = "INSERT INTO calendar (idDay,idMaster, freeTime)" \
            " VALUES ( \"%s\",  %i, \"%s\")" % (idDay,idMaster, freeTime)
    print(q)
    executeQuery(q)

def updateRating(id, ass):#перенесла функцию в keyboard
    q = "Select rating, countClient from master " \
        "WHERE id = %i" %id
    executeQuery(q)
    rt = 0; count = 0
    result = cur.fetchall()
    for row in result:
        rt = row[0]
        count = row[1]
    newRt = (rt*count + ass)/(count+1)
    q = "UPDATE master SET rating = %i, countClient = %i " \
        "WHERE id = %i" % (newRt, count+1, id)
    executeQuery(q)


if __name__ == '__main__':
    # создаем бд
    # conn = connect(host='localhost',
    #                user='root',
    #                password='87654W!')

    #БД НУРИИ:)
    conn = connect(host='localhost',
                   user='root')

    cur = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS `dbbeautysalon`"
    executeQuery(query)
    #подключаемся к нашей бд
    # conn = connect(host='localhost',
    #                        user='root',
    #                        password='87654W!',
    #                        database='dbbeautysalon')

    # БД НУРИИ:)
    conn = connect(host='localhost',
                   user='root',
                   database='dbbeautysalon')

    cur = conn.cursor()

    query = "DROP TABLE IF EXISTS master, service, calendar, record;"
    executeQuery(query)

    query = "CREATE TABLE master(" \
            "id INT AUTO_INCREMENT PRIMARY KEY," \
            "lastname VARCHAR(50)," \
            "name VARCHAR(50)," \
            "service VARCHAR(50)," \
            "isTop BOOL," \
            "rating DOUBLE," \
            "countClient int)"
    executeQuery(query)

    query = "CREATE TABLE service(" \
            "id INT AUTO_INCREMENT PRIMARY KEY," \
            "name VARCHAR(50)," \
            "priceTop INT," \
            "price INT," \
            "time INT)" #TIME
    executeQuery(query)

    query = "CREATE TABLE record(" \
            "idUser INT ," \
            "idMaster INT," \
            "idService INT," \
            "time VARCHAR(50), " \
            "idDay DATETIME, " \
            "CONSTRAINT PK_record PRIMARY KEY (idUser, idMaster,idService,idDay),"\
            "FOREIGN KEY(idMaster) REFERENCES master(id)," \
            "FOREIGN KEY(idService) REFERENCES service(id))"
    executeQuery(query)

    query = "CREATE TABLE calendar(" \
            "idDay Datetime ," \
            "idMaster INT," \
            "freeTime VARCHAR(50)," \
            "CONSTRAINT PK_calendar PRIMARY KEY ( idMaster,idDay)," \
            "FOREIGN KEY(idMaster) REFERENCES master(id))"

    executeQuery(query)

    insertMaster("Растремина", "Анастасия", "маникюр,педикюр", False, 0, 0)
    insertService("маникюр", 2000, 1000, 3)
    insertService("педикюр", 2500, 1500, 3)
    insertService("наращивание ресниц", 3500, 2200, 5)
    insertService("эпиляция", 900, 500, 1)
    insertMaster("Пупкина", "Васелина", "наращивание ресниц", False, 0, 0)
    insertMaster("Чушкина", "Маргарита", "маникюр,педикюр", True, 0, 0)
    insertMaster("Небукина", "Ирина", "эпиляция", False, 0, 0)

    insertClient(168671681, 1, 1, '13',  date(2021, 12, 2))

    insertCalendar(date(2021, 12, 7), 1, "0-14")
    insertCalendar(date(2021, 12, 8), 1, "0-14")
    insertCalendar(date(2021, 12, 9), 2, "0-14")
    insertCalendar(date(2021, 12, 10), 2, "0-14")
    insertCalendar(date(2021, 12, 11), 1, "0-14")
    insertCalendar(date(2021, 12, 12), 1, "0-14")
    insertCalendar(date(2021, 12, 13), 2, "0-14")
    insertCalendar(date(2021, 12, 14), 2, "0-14")
    insertCalendar(date(2021, 12, 7), 3, "14-24")
    insertCalendar(date(2021, 12, 8), 3, "14-24")
    insertCalendar(date(2021, 12, 9), 4, "14-24")
    insertCalendar(date(2021, 12, 10), 4, "14-24")
    insertCalendar(date(2021, 12, 11), 3, "14-24")
    insertCalendar(date(2021, 12, 12), 3, "14-24")
    insertCalendar(date(2021, 12, 13), 4, "14-24")
    insertCalendar(date(2021, 12, 14), 4, "14-24")
    # допустим знаем id мастера, обновляем рейтинг и кол-во клиентов
    updateRating(1,5)

    # получаем список услуг, цену
    q = "Select name, priceTop, price from service"
    executeQuery(q)
    result = cur.fetchall()
    for row in result:
        print(row[0], row[1], row[2])

    q = "Select * from calendar"
    executeQuery(q)
    result = cur.fetchall()
    for row in result:
        print(row[0], row[1], row[2])

