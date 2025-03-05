import time
from multiprocessing import Process, Queue


def write(q):
    users = ['杨勉琪', '牛魔', '哪吒', '李白', '娜可露露', '火舞', '暃', '孙悟空', '杨玉环', '小乔']
    for name in users:
        q.put(name)  # 存放信息
        print(f'收到数据{name}')


def read(q):
    while True:
        if not q.empty():
            values = q.get()  # 获取信息
            print(f'{values}是获取到的信息')
        else:
            break


if __name__ == '__main__':
    satr = time.time()
    q = Queue(10)
    w = Process(target=write, args=(q,))
    r = Process(target=read, args=(q,))
    w.start()
    r.start()
    w.join()
    r.join()
    print(f'所耗时间{time.time() - satr}')
