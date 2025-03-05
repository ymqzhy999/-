import json
import multiprocessing

import time

users = ['杨勉琪', '牛魔', '哪吒', '李白', '娜可露露', '火舞', '暃', '孙悟空', '杨玉环', '小乔']


def search(name):
    # time.sleep(1.6)
    data = json.load(open('db.txt', 'r', encoding='utf-8'))
    print(f'{name}正在查看票源,当前剩余票数为{data['count']}')


def get(name):
    data = json.load(open('db.txt', 'r', encoding='utf-8'))
    if data['count'] > 0:
        data['count'] -= 1
        print('正在出票,请稍后....')
        # time.sleep(2)
        print(f'购票成功 还剩{data['count']}')
        json.dump(data, open('db.txt', 'w'))
    else:
        print(f'今日票已售空-------{name}购票失败')


def func(name, l):
    l.acquire()
    search(name)
    get(name)
    l.release()


if __name__ == '__main__':
    star = time.time()
    for i in users:
        l = multiprocessing.Lock()
        people = multiprocessing.Process(target=func, args=(i, l))
        people.start()
        people.join()
    print(f'{time.time() - star}')
