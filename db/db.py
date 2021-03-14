#  Импортируем библиотеку SQLAlchemy
import sqlalchemy


# Создаем базу данных
def create_database(db_name):
    postgres = "yourself postgres"
    localhost = "yourself localhost"
    try:
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{postgres}@localhost:{localhost}/postgres")
        connection = engine.connect()
        connection.execute("commit")
        connection.execute(f"create database {db_name}")
        connection.close()
        # Создаем подключение к созданной базе данных
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{postgres}@localhost:{localhost}/{db_name}")
        connection = engine.connect()
        create_table(connection)
        return connection
    except sqlalchemy.exc.ProgrammingError:
        # Создаем подключение к созданной базе данных
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{postgres}@localhost:{localhost}/{db_name}")
        connection = engine.connect()
        return connection


# Создание таблиц
def create_table(arg):
    # Таблица id пользователей и их url
    arg.execute("""CREATE TABLE IF NOT EXISTS user_id (
    id SERIAL PRIMARY KEY,
    url_id VARCHAR(50) NOT NULL UNIQUE);""")

    # Таблица photo_url пользователей
    arg.execute("""CREATE TABLE IF NOT EXISTS photo (
    id SERIAL REFERENCES user_id(id),
    photo_url text );""")


#  Заполнение таблиц
def insert_data(arg_1, arg):
    for i in arg:
        uid, url = i.items()
        insert = f"INSERT INTO user_id(id, url_id) VALUES('{uid[0]}', '{uid[1]}');"
        arg_1.execute(insert)
        for photo in url[1]:
            insert = f"INSERT INTO photo(id, photo_url) VALUES('{uid[0]}', '{photo}');"
            arg_1.execute(insert)


# Получение списка id из базы данных
def select_user_id(arg):
    list_id = []
    for i in arg.execute("""SELECT id FROM user_id""").fetchall():
        list_id.append(i[0])
    return list_id
