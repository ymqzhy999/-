from multiprocessing import Process

age = 10


def func():
    global age
    age += 10
    print(f'子进程参数为{age}')


if __name__ == '__main__':
    p = Process(target=func)

    p.start()
    p.join()
    print(f"主进程age为{age}")

# 子进程参数为20
# 主进程age为10  不同进程都有不同的空间
