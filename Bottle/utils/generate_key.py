import random


def generate_app_key(user_id):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set + [str(user_id)]

    value_set = "".join(random.sample(total_set, 20))

    return value_set


def generate_verify_code():
    s = '0123456789'
    l = [random.choice(s) for i in range(4)]
    return ''.join(l)


if __name__ == '__main__':
    print(generate_app_key(1))
    print(generate_verify_code())