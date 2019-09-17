import asyncio
import random


async def mycoro(id):
    rnd = random.randint(1,10)
    print(f"Starting {id} - {rnd}")
    await asyncio.sleep(rnd)
    print(f"Finishing {id} - {rnd}")

async def main():
    coros = [mycoro(chr(x)) for x in range(65,85)]
    await asyncio.gather(*coros)



asyncio.run(main())
