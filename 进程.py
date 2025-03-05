"""
父子进程. 就是在一个进程的基础上创建出另一条完全独立的进程，这个就是子进程，相当于父进程的副本。
"""

import os
import time
from multiprocessing import Process

"""
    p1.daemon=True恶魔守护  用在开启同步阻塞之上  主进程结束 子进程也结束
    p1.join()天使守护 用在开启同步阻塞之后  等待所有子进程运行完  主进程才能结束
    且天使守护比恶魔作用强

"""


# 孤儿进程 主进程结束 子进程继续
def func(name):
    time.sleep(3)
    print(f"子进程是{name}")
    print(f'子进程id为:{os.getpid()}')  # os.getpid获取当前进程id
    print(f'主进程id为:{os.getppid()}')  # getppid()在子进程中获取主进程的编号  获取到的编号和主进程的编号相同是父子关系


if __name__ == '__main__':
    print('主进程')
    p1 = Process(target=func, args=("杨勉琪",))  # target是任务名  args传递任务参数 因为是元组类型 所以单个元组要加逗号
    p2 = Process(target=func, args=("印皓阳",))

    # p1.daemon=True
    # p2.daemon=True

    # 开启同步阻塞
    p1.start()
    p2.start()

    # p1.join()
    # p2.join()
    print('主进程gg')

age = 10


def func1():
    global age
    age += 10
    print(f'子进程{age}')


if __name__ == '__main__':
    p3 = Process(target=func1)

    p3.start()
    p3.join()
    print(f'主进程{age}')

"""
父子进程互不干扰 就算在进行
"""
