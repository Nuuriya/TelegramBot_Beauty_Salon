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
        "VALUES (\"%s\", %i, %i, \"%s\")" % (name, priceTop, price, time)
    print(q)
    executeQuery(q)
def updateRating(id, ass):
    q = "Select rating, countClient from master " \
        "WHERE id = %i" % (id)
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
                   password='root')
    cur = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS `dbbeautysalon`"
    executeQuery(query)
    #подключаемся к нашей бд
    conn = connect(host='localhost',
                           user='root',
                           password='root',
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
            "id INT AUTO_INCREMENT PRIMARY KEY," \
            "idMaster INT," \
            "idService INT," \
            "idDay INT," \
            "time int," \
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
    insertService("маникюр", 2000, 1000, "3")

    # допустим знаем id мастера, обновляем рейтинг и кол-во клиентов
    updateRating(1,5)

    # получаем список услуг, цену
    q = "Select name, priceTop, price from service"
    executeQuery(q)
    result = cur.fetchall()
    for row in result:
        print(row[0], row[1], row[2])


