import unittest
from vk import User
import vk_api


class MyTestCase(unittest.TestCase):

    def setUp(self):
        print("method setUp")
        self.token = "enter yourself token"     # введите свой токен
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk_session.get_api()
        self.vk_auth = self.vk_session.get_api()
        self.users_id = self.vk_auth.users.get(fields="bdate, sex, city, relation")
        self.uid = self.users_id[0].get('id')
        self.search_terms = {'age_from': 39, 'age_to': 43, 'city': 'Москва', 'sex': 2}

    def tearDown(self):
        print("method tearDown")

    def test_users_id(self):
        self.assertListEqual(User.users_id(self), self.users_id)

    def test_requirements(self):
        list_requirements = [{"sex": 1, "bdate": "25.4.1980", "city": {"id": 1, "title": "Москва"}, "relation": 1}]
        self.assertDictEqual(User.requirements(list_requirements), self.search_terms)

    def test_user_search(self):
        self.assertDictEqual(User.user_search(self, self.search_terms, [])[0],
                             {109630621: 'https://vk.com/id109630621'})

    def test_top_photo(self):
        list_candidates = [{"304063054": "https://vk.com/id304063054"}]
        top_photo_result = [{"304063054": "https://vk.com/id304063054",
                             "url_photo": ["https://sun9-36.userapi.com/impf/c625723/v625723054/2a1f5/EIF0Y5hEJ20.jpg"
                                           "?size=1280x854&quality=96&sign=e1317e80685534fc396b76d2effed76f&c_uniq_tag="
                                           "Uye9OaOk4w-AVw2bWD5DgPi3YjbyDvnSRHyReAervAI&type=album",
                                           "https://sun9-71.userapi.com/impf/c625724/v625724054/2f7f0/G7ynNhPpBPA.jpg?"
                                           "size=1280x960&quality=96&sign=25f8ebe22c27e351c2fd907cb140474d&c_uniq_tag="
                                           "6RGHpJQB0ECjBzZaOGm9PWuWWWQCIddGBnhA9fpw0ZI&type=album"]}]

        self.assertListEqual(User.top_photo(self, list_candidates), top_photo_result)


if __name__ == '__main__':
    unittest.main()
