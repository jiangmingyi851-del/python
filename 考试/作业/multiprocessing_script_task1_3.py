import multiprocessing

def consumer(q):
    while True:
        # 代码填空：从队列中获取数据
        item =q.get()
        if item == 'STOP':
            break
        print(f"消费: {item}")

def producer(q):
    for i in range(3):
        # 代码填空：向队列中添加数据，内容为"产品i"
        q.put(f"产品{i}")

    q.put('STOP')

if __name__ == '__main__':
    # 代码填空：创建一个队列
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
