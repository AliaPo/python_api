import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Editing user's cases")
class TestUserEdit(BaseCase):

    @allure.title("Test editing just created user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT

        new_name = "Changed Name"

        response3 = MyRequests.put(f"user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data = {"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 = MyRequests.get(f"user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )

        Assertions.assert_json_value_by_name(response4, 'firstName',
                                             new_name, 'Wrong name of the user after edit')

    @allure.title("Test editing another unauthorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_other_user(self):

        new_name = "Changed Name"

        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        authorization_response = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(authorization_response, "auth_sid")
        token = self.get_header(authorization_response, "x-csrf-token")
        id_value = self.get_json_value(authorization_response, "user_id")

        second_data = self.prepare_registration_data()

        registration_response = MyRequests.post("user/", data=second_data)
        second_authorization_response = MyRequests.post("user/login", data=second_data)

        edit_response = MyRequests.put(f"user/{id_value}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data = {"firstName": new_name})

        error_text = self.get_json_value(edit_response, "error")

        Assertions.assert_code_status(edit_response, 400)
        assert error_text == "Please, do not edit test users with ID 1, 2, 3, 4 or 5.", 'Wrong text for editing of the main users'

    @allure.title("Test editing email to invalid version")
    @allure.severity(allure.severity_level.MINOR)
    def test_edit_email_the_same_user(self):

        new_email = 'somebodyexample.com'
        data = self.prepare_registration_data()
        registration_response = MyRequests.post("user/", data=data)
        authorization_response = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(authorization_response, "auth_sid")
        token = self.get_header(authorization_response, "x-csrf-token")
        id_value = self.get_json_value(authorization_response, "user_id")

        edit_response = MyRequests.put(f"user/{id_value}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data = {"email": new_email})

        error_text = self.get_json_value(edit_response, "error")

        Assertions.assert_code_status(edit_response, 400)
        assert error_text == "Invalid email format", 'Wrong message for changing email to invalid version'

    @allure.title("Test editing first name to invalid version")
    @allure.severity(allure.severity_level.MINOR)
    def test_edit_name_to_short_version(self):
        new_name = 'M'

        data = self.prepare_registration_data()
        registration_response = MyRequests.post("user/", data=data)
        authorization_response = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(authorization_response, "auth_sid")
        token = self.get_header(authorization_response, "x-csrf-token")
        id_value = self.get_json_value(authorization_response, "user_id")

        edit_response = MyRequests.put(f"user/{id_value}",
                                           headers={"x-csrf-token": token},
                                           cookies={"auth_sid": auth_sid},
                                           data={"firstName": new_name})

        error_text = self.get_json_value(edit_response, "error")

        Assertions.assert_code_status(edit_response, 400)
        assert error_text == "The value for field `firstName` is too short", 'Wrong message for changing name to invalid version'




















