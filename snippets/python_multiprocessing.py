from multiprocessing import Pool
import time

COUNT = 50000000
def countdown(n):
    while n>0:
        n -= 1

if __name__ == '__main__':
    num = 5
    pool = Pool(processes=num)
    start = time.time()
    [pool.apply_async(countdown, [COUNT/num]) for _ in range(num)]

    #r1 = pool.apply_async(countdown, [COUNT/num])
    #r2 = pool.apply_async(countdown, [COUNT/3])
    #r3 = pool.apply_async(countdown, [COUNT/3])

    pool.close()
    pool.join()
    end = time.time()
    print('Time taken in seconds -', end - start, ' - ',num)
