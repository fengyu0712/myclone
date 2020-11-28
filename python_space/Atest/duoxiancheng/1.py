import threading
import time
import random
start_time =time.time()

def do_something():
    print ("{thread_name} start at {now}\n".format(thread_name=threading.currentThread().name,now=time.time()))
    time.sleep(1)
    print ("{thread_name} stop at {now}".format(thread_name=threading.currentThread().name,now=time.time()))


if __name__== "__main__":
    threads = []

    # start all threading.
    for i in range(1,8):
        t = threading.Thread(target=do_something)
        t.start()
        threads.append(t)

    #wait until all the threads terminnates.
    for thread in threads:
        thread.join()


    print ("all threads deid.")
    print ("this run take {t} seconds".format(t = (time.time()-start_time)))