import queue
from multiprocessing import Queue

# 创建进程通讯
# 创建Queue对象   无参数默认是存到内存爆炸 可以添加参数规定消息队列数
q = Queue(5)
# 存放数据
q.put(886)
q.put(666)
q.put('sbwy')
q.put('nbdl')
q.put('wan')  # 当存放数小于等于消息队列总数  运行成功
# q.put('满额')#如过超过总数 则会进入阻塞
try:
    q.put_nowait(1)  # 检查是否还能存放数据 如果不能就抛出异常queue.Full
except queue.Full:
    print('消息满额')

print(q.full())  # 判断消息队列是否满额 True
print(q.qsize())  # 消息数 5
print(q.get())  # 获取到第一条消息
