import pymysql
from pymysql import connect
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
def insertClient(idUser, idMaster, idService, idDay, time, date):
    q = "INSERT INTO record (name, priceTop, price, time) " \
        "VALUES (\"%s\", %i, %i, %i, %i, %i)" % (idUser, idMaster, idService, idDay, time, date)
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
    conn = connect(host='localhost',
                   user='root',
                   password='87654W!')

    #БД НУРИИ:)
    # conn = connect(host='localhost',
    #                user='root')

    cur = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS `dbbeautysalon`"
    executeQuery(query)
    #подключаемся к нашей бд
    conn = connect(host='localhost',
                           user='root',
                           password='87654W!',
                           database='dbbeautysalon')

    # БД НУРИИ:)
    # conn = connect(host='localhost',
    #                user='root',
    #                database='dbbeautysalon')

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
            "idDay INT," \
            "time int," \
            "date DATETIME," \
            "CONSTRAINT PK_record PRIMARY KEY (idUser, idMaster,idService,idDay),"\
            "FOREIGN KEY(idMaster) REFERENCES master(id)," \
            "FOREIGN KEY(idService) REFERENCES service(id))"
    executeQuery(query)

    query = "CREATE TABLE calendar(" \
            "id INT AUTO_INCREMENT PRIMARY KEY," \
            "idMaster INT," \
            "freeTime VARCHAR(50)," \
            "dayWeek INT," \
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

    insertClient(168671681, 1, 1, 1, 1, '2021-12-02 14:25:00')
    # допустим знаем id мастера, обновляем рейтинг и кол-во клиентов
    updateRating(1,5)

    # получаем список услуг, цену
    q = "Select name, priceTop, price from service"
    executeQuery(q)
    result = cur.fetchall()
    for row in result:
        print(row[0], row[1], row[2])


