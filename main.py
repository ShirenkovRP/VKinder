from pprint import pprint
import vk
from db import db


def main():
    # Входные данные
    mylogin = input("Введите номер телефона: ")
    mypassword = input("Введите пароль: ")

    print("\nНачинаем поиск")
    vk_auth = vk.vk(mylogin, mypassword)
    user_vk = vk.User(vk_auth)
    user_id = user_vk.users_id()
    search_term = user_vk.requirements(user_id)
    con = db.create_database("db_vk")
    elimination_id = db.select_user_id(con)
    user_search = user_vk.user_search(search_term, elimination_id)
    user_top_photo = user_vk.top_photo(user_search)

    print("\nРезультаты поиска")
    pprint(user_top_photo)

    # JSON-файл с 10 объектами, где у каждого объекта перечислены топ-3 фотографии и ссылка на аккаунт.
    vk.write_json(user_top_photo)

    # Запись в базу данных
    db.insert_data(con, user_top_photo)


if __name__ == '__main__':
    main()
