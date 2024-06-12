import pytest
import requests
class TestTasks:

    def test_input_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, 'Phrase should be shorter than 15 symbols'

    def test_cookie_method(self):

        expected_cookie_name = 'hw_value'

        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = dict(response.cookies)
        print(cookie)

        current_cookie_name = cookie["HomeWork"]
        assert current_cookie_name == expected_cookie_name, "Current cookie value is not equal to expected value"


    def test_method_header(self):

        headers_value = "Some secret value"

        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        current_headers = response.headers['x-secret-homework-header']
        print(current_headers)

        assert headers_value == current_headers, "Headers value is not equal to expected value"


    user_agent_data = [
        (
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
        (
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
        (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
        (
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]

    @pytest.mark.parametrize("user_agent, expected_values", user_agent_data)
    def test_user_agent(self, user_agent, expected_values):

        user_agents_with_wrong_params = []

        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                                headers={"User-Agent": user_agent})
        response_data = response.json()

        for key in expected_values:
            if response_data[key] != expected_values[key]:
                user_agents_with_wrong_params.append(
                    {
                        'user_agent': user_agent,
                        'wrong_param': key,
                        'expected_param': expected_values[key],
                        'actual_value': response_data[key]
                    }
                )

        if user_agents_with_wrong_params:
            pytest.fail(str(user_agents_with_wrong_params))