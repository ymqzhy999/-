import os
from multiprocessing import Process


def func():
    print('子进程')
    # 获取当前的进程编号
    print(f'子进程当前的进程编号为:{os.getpid()}')
    print(f'子进程所在的主进程编号为：{os.getppid()}')


if __name__ == '__main__':
    print('主进程开始')
    print(f'主进程当前的进程编号{os.getpid()}')
    p = Process(target=func)
    p.start()
    p.join()
    print('主进程结束')

# 因为主进程的编号和子进程所在的主进程编号相同 所以他们处于同一进程中
