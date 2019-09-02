import asyncio
import time
import datetime

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(f"{what} {time.strftime('%X')}")
    await asyncio.sleep(3)
    print(what)
    
async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(
        say_after(10, 'hello'))

    task2 = asyncio.create_task(
        say_after(5, 'world'))

    task3 = asyncio.create_task(say_after(3,f'Chamada 1'))

    task4 = asyncio.create_task(say_after(1,f'Chamada 2'))

    task5 = asyncio.create_task(display_date())
    
    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task3
    await task4
    await task1
    await task5
    await task2




    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
