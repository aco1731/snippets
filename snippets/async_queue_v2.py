import asyncio, random, time

async def rnd_sleep(t):
    # sleep for T seconds on average
    await asyncio.sleep(t * random.random() * 2)

async def producer(queue):
    while True:
        token = round(random.random() * 10)
        print(f'produced {token}')
        if token < 1:
            break
        if not(token % 2):
            await queue.put((0,token))
        else:
            await queue.put((1,token))
        await rnd_sleep(0.5)

async def consumer(queue):
    while True:
        token = await queue.get()
        await rnd_sleep(.5)
        queue.task_done()
        print(f'consumed {token}')

async def main():
    queue = asyncio.PriorityQueue()

    # fire up the both producers and consumers
    producers = [asyncio.create_task(producer(queue))
                 for _ in range(5)]
    consumers = [asyncio.create_task(consumer(queue))
                 for _ in range(1)]

    # with both producers and consumers running, wait for
    # the producers to finish

    await asyncio.gather(*producers)
    print('---- done producing')

    # wait for the remaining tasks to be processed
    await queue.join()

    # cancel the consumers, which are now idle
    for c in consumers:
        c.cancel()

asyncio.run(main())
