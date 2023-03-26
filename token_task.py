import json
import time

import requests

response_first = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
print(response_first.text)

json_resp = json.loads(response_first.text)
token_value = json_resp["token"]
time_to_sleep = json_resp["seconds"]

params = {"token": token_value}

response_second = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=params)
print(response_second.text)
json_resp_sec = json.loads(response_second.text)
status_value_sec = json_resp_sec['status']
if status_value_sec == "Job is NOT ready":
    print('Status is correct')
else:
    print('Status is wrong')

time.sleep(int(time_to_sleep))
response_third = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=params)
print(response_third.text)
json_resp_third = json.loads(response_third.text)
status_value_third = json_resp_third['status']
result_value = json_resp_third['result']
if status_value_third == "Job is ready":
    if len(result_value) != 0:
        print('There is result')
    else:
        print('There is no any results')
    print('Final status is correct')
else:
    print('Final status is wrong')

