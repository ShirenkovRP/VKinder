import time
from db import db
import vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

mylogin = "yourself login"
mypassword = "yourself password"
token_group = "yourself token group"


def show_poto(arg):
    list_0 = []
    for i in arg:
        uid, url = i.items()
        photo_url = list(url[1][0].items())[0][0]
        list_0.append([uid[0], f"photo{uid[0]}_{photo_url}"])
    return list_0


def main():
    while True:
        con = db.create_database("db_vk")
        elimination_id = db.select_user_id(con)

        receive_message = vk.Communication(token_group).listen()
        sending_message = vk.Communication(token_group)
        admin_group = vk.User(mylogin, mypassword)
        mess_id = receive_message[0]

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('поиск кандидатов', color=VkKeyboardColor.SECONDARY)

        sending_message.send_message(mess_id, "нажмите на поиск кандидатов ", keyboard=keyboard.get_keyboard())

        if receive_message[1] == "поиск кандидатов":
            user_vk = admin_group.users_id(mess_id)
            search_term = admin_group.requirements(user_vk)

            # запрашиваем не достающую информацию
            # возраст
            if search_term["age_from"] is None and search_term["age_to"] is None:
                sending_message.send_message(mess_id, f"Не хватает данных для поиска")
                sending_message.send_message(mess_id, f"Введите свой возраст")
                receive_message = vk.Communication(token_group).listen()
                search_term["age_from"] = int(receive_message[1]) - 2
                search_term["age_to"] = int(receive_message[1]) + 2

            # пол
            if search_term["sex"] is None:
                sending_message.send_message(mess_id, f"Укажите пол для поиска")
                sending_message.send_message(mess_id, f"Выбирите одну из цифр")
                sending_message.send_message(mess_id, f"1 - женский 2 - мужской")
                receive_message = vk.Communication(token_group).listen()
                search_term["sex"] = int(receive_message[1])

            # город
            if search_term["age_to"] is None:
                sending_message.send_message(mess_id, f"Укажите город для поиска")
                sending_message.send_message(mess_id, f"Введите название города")
                receive_message = vk.Communication(token_group).listen()
                search_term["city"] = receive_message[1]

            # Отбор кандидатов и выбор 3 фото
            sending_message.send_message(mess_id, f"идет поиск кандидатов")
            user_search = admin_group.user_search(search_term, elimination_id)
            user_top_photo = admin_group.top_photo(user_search)

            # JSON-файл с 10 объектами, где у каждого объекта перечислены топ-3 фотографии и ссылка на аккаунт.
            vk.write_json(user_top_photo)

            # Запись в базу данных
            db.insert_data(con, user_top_photo)

            # Показ фото кандидатов
            photo_candidates = show_poto(user_top_photo)
            count = 0
            while count < len(photo_candidates):
                show_id = photo_candidates[count][0]
                show_can = admin_group.users_id(show_id)
                first_name = show_can[0].get("first_name")
                last_name = show_can[0].get("last_name")
                sending_message.send_message(mess_id, f"{first_name} {last_name}")
                sending_message.send_message_media(mess_id, photo_candidates[count][1])
                time.sleep(1)
                count += 1
            sending_message.send_message(mess_id, f"поиск окончен")


if __name__ == '__main__':
    main()
