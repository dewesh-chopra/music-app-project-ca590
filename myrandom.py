import random


def randomnum():
    num = random.randrange(1000, 9999)
    return num

def randomalphanum():
    vals = "abcdefghijklmnopqrstuvwxyz0123456789"
    s = ""
    for i in range(0, 4):
        index = random.randrange(0, 36)
        s = s + vals[index]
    return s
