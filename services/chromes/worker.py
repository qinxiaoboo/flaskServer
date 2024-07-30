from flaskServer.config.config import THREAD_POOL_NUM
from concurrent.futures import ThreadPoolExecutor
import time
from loguru import logger

executor = ThreadPoolExecutor(THREAD_POOL_NUM)

# def worker(data,name,age,key="key",value="value"):
#     print(data)
#     print(name,age,key,value)

def submit(func,datas,*args, **kwargs):
    fs = []
    with executor:
        for data in datas:
            f = executor.submit(func,data, *args, **kwargs)
            fs.append(f)
        while True:
            time.sleep(3)
            flag = True
            for f in fs:
                flag = flag and f.done()
                if not flag:
                    break
            if flag:
                break
        # for f in fs:
        #     logger.info('{} result = {}'.format(f, f.result()))


if __name__ == '__main__':
    pass
    # submit(worker,["test","text"],"qinxiaobo","28",key="change",value="old")

