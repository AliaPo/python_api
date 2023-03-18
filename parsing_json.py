import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(json_text)
obj_parsed = obj['messages']
obj_parsed_second_key = obj_parsed[1]
print(obj_parsed_second_key['message'])