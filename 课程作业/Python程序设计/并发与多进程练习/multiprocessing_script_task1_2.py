import multiprocessing

def square(x):
    return x * x

if __name__ == '__main__':
    # 代码填空：创建一个进程池，进程数为4
    with multiprocessing.Pool(4) as pool:
        results = [pool.apply_async(square, (i,)) for i in range(5)]
        output = [res.get() for res in results]
    print(output)  # 应该输出 [0, 1, 4, 9, 16]
