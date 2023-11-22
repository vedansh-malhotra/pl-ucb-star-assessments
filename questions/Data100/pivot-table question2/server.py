import random

def generate(data):
    # Sample two random integers between 5 and 10 (inclusive)
    a = random.randint(5, 10)
    b = random.randint(5, 10)

    # Put these two integers into data['params']
    data["params"]["a"] = a
    data["params"]["b"] = b
