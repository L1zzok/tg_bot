# импортируем библиотеку для работы с базой данных
import sqlite3

# создали подключение к бд. если такой базы нет, то она создастся сама
con = sqlite3.connect(r"db.db", check_same_thread=False)
# создали курсор для запросов
cursor = con.cursor()


# создали таблицу в базе, если она еще не существует
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "users" ("id" INTEGER NOT NULL,"login" TEXT NOT NULL, primary key("id" AUTOINCREMENT));''')
# создали таблицу категории в базе, если ее еще нет
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "categories" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"name" TEXT NOT NULL); ''')

# создали таблицу подписки в базе, если ее еще нет
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "subscribes" ( "id_user" INTEGER NOT NULL, "id_category" INTEGER NOT NULL, FOREIGN KEY ("id_user") REFERENCES users("id"), FOREIGN KEY ("id_category") REFERENCES categories("id") )''')
# зафиксировали изменения в базе
con.commit()


# функция поиска пользователя в базе
def find_user(cursor, login):
    return cursor.execute('''SELECT * FROM users WHERE login=?;''', (login,)).fetchone()


# функция регистрации пользователя
def registration(connection, cursor, login):
    if not find_user(cursor, login):
        cursor.execute(
            '''INSERT INTO users(login) VALUES (?) ;''', (login,))
    connection.commit()


# функция удаления пользователя
def delete_user(connection, cursor, login):
    # cursor.execute('''DELETE FROM subscribes WHERE id_user = (SELECT id FROM users WHERE login = ?);''', (login,))
    cursor.execute(
        '''DELETE FROM users WHERE users.login=?;''', (login,))
    connection.commit()


# функция по поиску категории
def find_category(cursor, name):
    return cursor.execute('''SELECT * FROM categories WHERE name=?;''', (name,)).fetchone()


# функция добавления категории
def insertCategory(connection, cursor, name):
    cursor.execute(
        '''INSERT INTO categories(name) VALUES (?);''', (name,))
    connection.commit()


# функция удаления категории
def delete_category(connection, cursor, name):
    cursor.execute(
        '''DELETE FROM categories WHERE name =?;''', (name,))
    connection.commit()


# функция по поиску категории в подписке
def find_category_in_sub(cursor,user,category):
    cat = cursor.execute('''SELECT * FROM subscribes WHERE id_user = (SELECT id FROM users WHERE login = ?) AND id_category =(SELECT id FROM categories WHERE name = ?) ;''',(user,category,)).fetchall()
    for i in cat:
        return i;

# функция поиску подписок юзера
def find_category_user(cursor,user):
    cat = cursor.execute('''SELECT id_category FROM subscribes WHERE id_user = (SELECT id FROM users WHERE login = ?);''',(user,)).fetchall()
    for i in cat:
        return i;

# функция подписки пользователя на категорию
def sub_category(connection, cursor, name, login):
    if find_category_in_sub(cursor, name, login) == None:
        cursor.execute(
            '''INSERT INTO subscribes (id_user, id_category) VALUES ((SELECT id FROM users WHERE login = ?), (SELECT id FROM categories WHERE name = ?))''',
            (login, name,)
        )
        connection.commit()


# функция отписки пользователя от категории
def unsub_category(connection, cursor, name, login):
    cursor.execute(
        '''DELETE FROM subscribes WHERE id_user = (SELECT id FROM users WHERE login = ?) AND id_category = (SELECT id FROM categories WHERE name = ?)''',
        (login, name,)
    )
    connection.commit()


# функция просмотра подписок на категории пользователя
def look_sub(cursor, login):
    cat = cursor.execute(
        '''SELECT categories.name FROM subscribes INNER JOIN categories ON id_category = categories.id WHERE id_user = (SELECT id FROM users WHERE login = ?)''',
        (login,)
    ).fetchall()
    categ = list()
    for i in cat:
        categ.append(i[0])
    return categ


# вывод всех категорий
def all_categories(cursor):
    cat = cursor.execute('''SELECT name FROM categories''').fetchall()
    categ = list()
    for i in cat:
        categ.append(i[0])
    return categ


# закрыли подключение
con.close()





