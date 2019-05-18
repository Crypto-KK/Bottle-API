import random
from datetime import datetime


def generate_app_key(user_id):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set + [str(user_id)]

    value_set = "".join(random.sample(total_set, 20))

    return value_set


if __name__ == '__main__':
    print(generate_app_key(1))