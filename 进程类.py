from multiprocessing import Process


class MyProcess(Process):
    def __init__(self, name):
        super().__init__()  # 要继承Process类中的方法
        self.name = name

    def eat(self, name):
        print(f'等下{name}去吃火锅')

    def sport(self, name):
        print(f'{name}刚在跑步')

    # 重写run方法
    # 把子进程执行的任务放到这里面进行调用
    def run(self):
        print('我是自定义的进程类的子进程')
        self.eat(self.name)
        self.sport(self.name)


if __name__ == '__main__':
    p = MyProcess('杨勉琪')

    p.start()  # 启动我们的进程  start执行的就是进程类中的run方法
