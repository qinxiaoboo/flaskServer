

def getUserAgent():
    s = set()
    with open(r'D:\python\wf-chrome\flaskServer\utils\useragent.txt','r') as f:
        for line in f:
            s.add(line.strip())
    return s.pop()

if __name__ == '__main__':
    print(getUserAgent())

