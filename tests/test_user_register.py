import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.randomizer import random_str, random_email

@allure.epic("Create user's cases")
class TestUserRegister(BaseCase):

    @allure.title("Test successfully creating user")
    @allure.description("This test creates user with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_create_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.title("Test creating user with the existing email")
    @allure.description("This test checks creating user with the same email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", \
            f"Unexpected response content: {response.content}"

    @allure.title("Test creating user with incorrect email")
    @allure.description("This test checks creating user with the invalid email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format", \
            f"Unexpected response content: {response.content}"

    @allure.title("Test creating user with the short name")
    @allure.description("This test checks creating user with one symbol name")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data(name='T')

        response = MyRequests.post("user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.title("Test creating user with the long name")
    @allure.description("This test checks creating user with one symbol name")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_long_name(self):
        long_name = random_str(250)
        data = self.prepare_registration_data(name=long_name)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')


    data = [({'firstName': 'learnqa', 'lastName': 'learnqa',
              'email': f'{random_email()}', 'password': '123'}),
            ({'username': f'{random_str(5)}', 'lastName': 'learnqa',
              'email': f'{random_email()}', 'password': '123'}),
            ({'username': f'{random_str(5)}', 'firstName': 'learnqa',
              'email': f'{random_email()}', 'password': '123'}),
            ({'username': f'{random_str(5)}', 'firstName': 'learnqa', 'lastName': 'learnqa',
              'password': '123'}),
            ({'username': f'{random_str(5)}', 'firstName': 'learnqa', 'lastName': 'learnqa',
              'email': f'{random_email()}'})
            ]

    @allure.title("Test creating user without one parameter")
    @allure.description("This test checks creating user without each possible parameter")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", data)
    def test_create_user_without_one_parameter(self, data):

        response = MyRequests.post("user/", data=data)
        first_answer_part = response.text.split(':')[0]

        Assertions.assert_code_status(response, 400)
        assert first_answer_part == 'The following required params are missed', 'Wrong answer while creating user with missing param'
