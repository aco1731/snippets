#!/usr/bin/env python3
# rand.py

import asyncio
import random


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(0)
        i = random.randint(0, 10)
    print(f"---> Finished: makerandom({idx}) == {i}")
    return i

async def main():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(5)))
    return res

if __name__ == "__main__":
    r1, r2, r3, r4, r5 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3} r4: {r4}, r5: {r5}")
