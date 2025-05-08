import random
import string


def generate_random_ascii(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


if __name__ == '__main__':
    print(generate_random_ascii(50))
