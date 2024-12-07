import random

def random_number():
    res = [str(random.randint(0, 10)) for i in range(10)]
    return "".join(res)