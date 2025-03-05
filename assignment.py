import time
s = 0


def make_population():
    for a in range(2000):
        global s
        s += a
    return s


start = time.time()
make_population()
make_population()
make_population()
end = time.time()
print(f'所耗时间{end - start}')

# def make_population():
#     s=0
#     for a in range(200):
#         s+=a
#     return s
#
#
# if __name__ =='__main__':
#     start1 = time.time()
#     ps = []
#     for i in range(3):
#         p = multiprocessing.Process(target=make_population)
#         ps.append(p)
#         p.start()
#     for p in ps:
#         p.join()
#     end = time.time()
#     print(f'所耗时间{end-start1}')
