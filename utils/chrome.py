import random

s = list()
with open(r'D:\python\wf-chrome\flaskServer\utils\useragent.txt', 'r') as f:
    for line in f:
        s.append(line.strip())

def getUserAgent():

    return random.choice(s)

if __name__ == '__main__':
    print(getUserAgent())

