import multiprocessing
import time
from multiprocessing import Pool, Manager

class CustomWorker:
    def __init__(self, worker_id, task_queue, result_queue, config):
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.__secret_key = config['key']
        self.__mode = config['mode']

    def run(self):
        # print(f"Worker {self.worker_id} started with mode {self.__mode}")
        while True:
            try:
                task = self.task_queue.get()
                if task == 'TERMINATE':
                    # print(f"Worker {self.worker_id} terminating")
                    break
                result = self.__process(task)
                self.result_queue.put({'worker': self.worker_id, 'result': result, 'task': task})
            except Exception as e:
                self.result_queue.put({'worker': self.worker_id, 'error': str(e), 'task': task})

    def __process(self, task):
        if self.__mode == 'encrypt':
            return f"{task}_{self.__secret_key}"
        elif self.__mode == 'hash':
            return hash(task + self.__secret_key)
        else:
            raise ValueError("Invalid mode")

def worker_process(task_queue, result_queue):
    worker_id = multiprocessing.current_process()._identity[0]
    config = {
        'key': f"KEY{worker_id}",
        'mode': 'encrypt' if worker_id % 2 == 0 else 'hash'
    }
    worker = CustomWorker(worker_id, task_queue, result_queue, config)
    worker.run()  

def main():
    manager = Manager()
    task_queue = manager.Queue()
    result_queue = manager.Queue()

    pool_size = 3
    
    # 先放入所有任务
    for i in range(20):
        task_queue.put(f"task_{i}")
    
    # 添加足够的终止信号
    for _ in range(pool_size):
        task_queue.put("TERMINATE")

    # 创建并启动进程池
    pool = Pool(
        processes=pool_size,
        initializer=worker_process,
        initargs=(task_queue, result_queue)
    )
    
    # 收集结果
    results = []
    tasks_processed = 0
    expected_tasks = 20  # 期望处理的任务数
    
    while tasks_processed < expected_tasks:
        result = result_queue.get()
        tasks_processed += 1
        
        if 'error' in result:
            print(f"Error from worker {result['worker']} processing {result['task']}: {result['error']}")
        else:
            results.append(result)
            # print(f"Worker {result['worker']} processed {result['task']} → {result['result']}")
    
    # 等待所有进程完成
    pool.close()
    pool.join()
    
    # print(f"Processed {len(results)} tasks successfully")
    print(f"Final results: {results}")

if __name__ == '__main__':
    main()
