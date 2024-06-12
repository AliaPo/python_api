import requests
list_of_methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
for meaning in list_of_methods:
    if meaning == 'GET':
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=meaning)
    else:
        response = requests.request(meaning, "https://playground.learnqa.ru/ajax/api/compare_query_type")
    print(f'Request made by using method {meaning} has status code {response.status_code}')
