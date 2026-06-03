#导入模块
import multiprocessing
import time
 
#创建进程调用函数
def work1(interval):
	print('执行work1')
	time.sleep(interval)
	print('end work1')
 
def work2(interval):
	print('执行work2')
	time.sleep(interval)
	print('end work2')
 
if __name__ == "__main__":
	print('执行主进程')
	#代码填空：创建进程对象
	p1=multiprocessing.Process(target=work1,args=(2,))
	p2=multiprocessing.Process(target=work2,args=(3,))
	#代码填空：启动进程
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	print('主进程结束')
