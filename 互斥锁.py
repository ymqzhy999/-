# 牺牲效率 提高数据安全

import json
import time
from multiprocessing import Process


def search(name):
    time.sleep(1)
    result = json.load(open('db.json', 'r', encoding='utf-8'))
    print(f'{name} {result['count']}')


def go(name):
    time.sleep(0.5)
    result = json.load(open('db.json', 'r', encoding='utf-8'))
    if result['count'] > 0:  # 查看是否已有对象
        print('追下一位')
    else:
        result['count'] += 1
        print(f'{name}追到了女神')
        json.dump(result, open('db.json', 'w', encoding='utf-8'))


def func(name, ):
    # 通过acquire 加锁资源
    # l.acquire()
    search(name)
    go(name)
    # l.release()#释放锁 让下一位也可以追


if __name__ == '__main__':
    # l=Lock()#给锁创建一个实例对象
    Li = ['杨勉琪', '印皓阳', '赵红帅', '火柴人', '沸羊羊',
          '霍金', '爱因斯坦'
          ]
    for i in Li:
        p = Process(target=func, args=(i,))
        p.start()
        p.join()

"""                         
有互斥锁                    


杨勉琪 1
追下一位
印皓阳 1
追下一位
赵红帅 1
追下一位
"""

"""
无互斥锁

杨勉琪 1
印皓阳 1
赵红帅 1
追下一位
追下一位
追下一位
"""
