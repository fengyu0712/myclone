import multiprocessing
from multiprocessing import Process

class MyProcess(Process):
    def __set__(self, func, args):
        super(MyProcess,self).__init__()
        self.func=func
        self.args=args
        self.res=''
        self.q = q
        # self._daemonic=True
        # self._daemonic=True
    def run(self):
        self.res=self.func(*self.args)
        self.q.put((self.func.__name__,self.res))

    def use_multiprocessing(func_list):
        # os.system('export PYTHONOPTIMIZE=1')  # 解决 daemonic processes are not allowed to have children 问题
        q = multiprocessing.Queue() # 队列,将多进程结果存入这里，进程间共享， 多进程必须使用  multiprocessing 的queue
        proc_list = []
        res=[]
        for func in func_list:
            proc = MyProcess(func['func'],args=func['args'],q = q)
            proc.start()
            proc_list.append(proc)

        for p in  proc_list:
            p.join()
        while not q.empty():
            r = q.get()
            res.append(r)
        return res
#使用时候，将需要多进程执行的函数和函数的参数当作字段，组成个list 传给use_multiprocessing 方法即可



