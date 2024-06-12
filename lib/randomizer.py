import random
import string

def random_str(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_email():
    first_part = random_str(8)
    second_part = '@example.com'

    return first_part + second_part