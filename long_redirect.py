import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
count_redirects = len(response.history)
final_url = response.url
print(count_redirects)
print(final_url)