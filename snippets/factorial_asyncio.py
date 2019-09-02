import asyncio
import time

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(0.01)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def print_time(x):
    for _ in range(x):
        print(f"TIME NOW: {time.strftime('%X')}")
        await asyncio.sleep(1)
    

async def main():
    
    # Schedule three calls *concurrently*:
    task5 = asyncio.create_task(print_time(5))

    print(f"started at {time.strftime('%X')}")

    
    await asyncio.gather(
        task5,
        factorial("A", 1000),
        factorial("B", 10),
        factorial("C", 100),
    )


    print(f"finished at {time.strftime('%X')}")



     
asyncio.run(main())
