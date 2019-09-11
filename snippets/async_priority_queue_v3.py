import asyncio, random, time

async def rnd_sleep(t):
    # sleep for T seconds on average
    await asyncio.sleep(t * random.random() * 2)

async def producer(queue,_):
    order = 0
    while True:
        token = round(random.random() * 5)
        
        if token < 1:
            print(f'produced{_} morreu!')
            break
        else:
            print(f'produced{_} - {token}')
            
        if not(token % 2): #Par tem prioridade.
            await queue.put((0,order, token))
        else:
            await queue.put((1,order, token))
        await rnd_sleep(1)
        order +=1

async def consumer(queue,_):
    while True:
        token = await queue.get()
        prioridade, cont, data = token
        await rnd_sleep(.5)
        queue.task_done()
        print(f'consumed{_} - FILA: {prioridade} POSIÇÃO: {cont} INFO: {data}')

async def main():
    queue = asyncio.PriorityQueue()

    # fire up the both producers and consumers
    producers = [asyncio.create_task(producer(queue,_))
                 for _ in range(2)]
    consumers = [asyncio.create_task(consumer(queue,_))
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
