import time
from multiprocessing import Process


def eat(name, num):
    print(f'{name}吃了第{num}碗了')


if __name__ == '__main__':
    start = time.time()
    # 主进程的for循环
    for i in range(10):
        p = Process(target=eat, args=('杨勉琪', i))
        p.start()
        p.join()  # 天使守护  造成同步阻塞 等待所有子进程运行完  主进程才能结束
    print(f'主进程结束{time.time() - start}')
