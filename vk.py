from datetime import datetime
import json
import time
import vk_api
# https://vk-api.readthedocs.io/en/latest/index.html# - ссылка на документацию vk_api


#  Получение токена для работы с API
def vk(login, password):
    try:
        scope = "FRIEND, PHOTOS, PAGES , STATUS, OFFLINE, DOCS, GROUPS"
        vk_session = vk_api.VkApi(login, password, scope=scope)
        vk_session.auth()
        return vk_session.get_api()
    except vk_api.exceptions.AuthError:
        print("Неверный логин или пароль")
        login = int(input("Введите номер телефона: "))
        password = input("Введите пароль: ")
        vk(login, password)


#   Создание возрастного диапазано  для поиска
def set_age():
    try:
        print('\nВведите возрастной диапазон')
        age_from = int(input('Возраст от: '))
        age_to = int(input('Возраст до: '))
        while age_to < age_from:
            print(f"Неверно указан возраст должен быть больше {age_from}")
            age_to = int(input('Возраст до: '))
        return age_from, age_to
    except ValueError:
        print("Должно быть целое число")
        set_age()


#  Запись результата в файл
def write_json(data_to_write):
    with open('top_10_users.json', 'w', encoding='utf-8') as file:
        json.dump(data_to_write, file, ensure_ascii=False, indent=2)


class User:

    def __init__(self, vk_auth):
        self.vk_auth = vk_auth

    # Получаем информацию о полтзователе
    def users_id(self, uid=None):
        user_information = self.vk_auth.users.get(user_ids=uid, fields="bdate, sex, city, relation")
        time.sleep(0.27)
        return user_information

    # Дополняем недостающю недостающую информацию
    # Составляем условия поиска
    @staticmethod
    def requirements(arg):
        requirements = {}
        # возраст
        age = arg[0].get('bdate')
        if age is not None and len(age.split(".")) == 3:
            year_birth = datetime.strptime(age, '%d.%m.%Y').year
            this_year = datetime.now().year
            requirements["age_from"] = this_year - year_birth - 2
            requirements["age_to"] = this_year - year_birth + 2
            print(f"Возраст от: {this_year - year_birth - 2}")
            print(f"Возраст до: {this_year - year_birth + 2}")
        else:
            age_1 = set_age()
            requirements["age_from"] = age_1[0]
            requirements["age_to"] = age_1[1]
        # пол
        sex = arg[0].get('sex')
        if sex == 1:
            sex = 2
            print(f"\nИщем мужчину")
        elif sex == 2:
            sex = 1
            print(f"\nИщем женщину")
        else:
            print("Укажите пол для поиска")
            sex = int(input("1 - женский 2 - мужской: "))
        requirements["sex"] = sex
        # город
        city = arg[0].get('city').get('title')
        if city is not None:
            requirements["city"] = city
            print(f"\nПроживает в {city}")
        else:
            print("Укажите город")
            city = input("Введите название города: ")
            requirements["city"] = city
        return requirements

    # Ищем 10 пользователей с подходящими условиями
    def user_search(self, arg, elimination_id):
        sex = arg["sex"]
        hometown = arg["city"]
        status = 1
        age_from = arg["age_from"]
        age_to = arg["age_to"]
        user_search = self.vk_auth.users.search(count=1000, hometown=hometown,
                                                sex=sex, status=status,
                                                age_from=age_from, age_to=age_to,
                                                fields="is_closed")
        time.sleep(0.27)
        address_list = []
        for i in user_search["items"]:
            address_dict = {}
            if i["can_access_closed"] and len(address_list) < 10:
                if i["id"] not in elimination_id:
                    address_dict[i["id"]] = "https://vk.com/id" + str(i["id"])
                    address_list.append(address_dict)
        return address_list

    # Добавляем топ 3 фото пользователя в список кандидатов
    def top_photo(self, list_candidates):
        for i in list_candidates:
            # Получаем список фото пользователя
            uid = i.keys()
            top3photo = self.vk_auth.photos.get(owner_id=uid, album_id="profile", extended=1)
            time.sleep(0.27)
            # Создаем список лайков и сортируем по убыванию
            likes_list = []
            for likes_i in top3photo["items"]:
                likes_list.append(likes_i["likes"]["count"])
            likes_list.sort(reverse=True)
            # Получаем три ссылки на фото с наибольшим кол-вом лайков
            list_url_photo = []
            for photo_i in top3photo["items"]:
                if photo_i["likes"]["count"] in likes_list[0: 3]:
                    list_url_photo.append(photo_i["sizes"][-1]["url"])
            # Добовляем список uri фото в список пользователей
            i["url_photo"] = list_url_photo
        return list_candidates
