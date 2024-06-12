import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Get user's details cases")
class TestUserGet(BaseCase):

    @allure.title("Test getting unauthorized user's info")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("user/2")

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    @allure.title("Test getting authorized user's info")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Test getting another user's info by authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_the_other_user_details(self):

        data = self.prepare_registration_data()

        response1 = MyRequests.post("user/", data=data)

        response2 = MyRequests.post("user/login", data=data)

        response3 = MyRequests.get("user/2")

        Assertions.assert_json_has_key(response3, 'username')
        Assertions.assert_json_has_no_key(response3, "email")
        Assertions.assert_json_has_no_key(response3, "firstName")
        Assertions.assert_json_has_no_key(response3, "lastName")

