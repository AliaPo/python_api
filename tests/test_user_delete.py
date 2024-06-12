from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Deleting cases")
class TestUserDelete(BaseCase):

    @allure.title("Test deleting one of the main users")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_the_main_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post('user/login', data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        delete_response = MyRequests.delete(f"user/{user_id_from_auth_method}",
                                            headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        text = self.get_json_value(delete_response, "error")

        Assertions.assert_code_status(delete_response, 400)
        assert text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", 'Wrong description for deleting on of the main users'

    @allure.title("Test deleting authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_authorized_user_pozitive_case(self):

        data = self.prepare_registration_data()

        registration_response = MyRequests.post("user/", data=data)
        authorization_response = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(authorization_response, "auth_sid")
        token = self.get_header(authorization_response, "x-csrf-token")
        id_value = self.get_json_value(authorization_response, "user_id")

        delete_response = MyRequests.delete(f"user/{id_value}",
                                            headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(delete_response, 200)

        get_info_response = MyRequests.get(f"user/{id_value}",
                                 headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(get_info_response, 404)
        assert get_info_response.text == 'User not found', 'Wrong answer for deleted user'

    @allure.title("Test deleting another user by authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_the_other_user(self):

        data = self.prepare_registration_data()

        registration_response = MyRequests.post("user/", data=data)
        authorization_response = MyRequests.post("user/login", data=data)

        delete_response = MyRequests.delete("user/2")

        Assertions.assert_code_status(delete_response, 400)
        Assertions.assert_json_has_key(delete_response, 'error')