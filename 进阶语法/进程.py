# 进程的相关概念

# 每个进程都有自己的资源,包括主进程,他们各自的资源空间不同,因此执行起来也互不影响
# 主进程在进行的时候默认执行;子进程可以开启p1=Process(target=task,args=())
# 真正的进程分配资源使用start(),启动资源使用run()方法,start()内部启动了调用run()方法进程共享全局变量
# 如果是全局变量,每个进程都会拥有一份全局变量,各自操作各自的全局变量,互不影响.
# Python 实现：通过 multiprocessing 模块创建和管理进程。
# 与线程的区别：进程间内存隔离，线程共享内存；进程更稳定但开销更大。
import multiprocessing
import time
import os
# 相关函数
#os.getpid()#获取当前进程号
#current_process().name:获取当前进程的名字
# os.getppid()获取父进程号
# start()为进程分配资源,通过run()方法启动进程
#run():只是一个普通的方法,通过调用该方法来启动进程执行
# join([timeout=seconds])  阻塞主进程后面的代码不执行
#is_alive():判断进程的任务是否完成
#kill()杀死进程
#terminate()#:终止进程
