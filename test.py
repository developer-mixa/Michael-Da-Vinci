import asyncio
import time
from datetime import datetime


async def temp():
    print('hello1')
    await asyncio.sleep(1)
    print('hello2')


background_tasks = set()


async def main():
    print(datetime.now())

    cor1 = temp()
    cor2 = temp()

    task1 = asyncio.create_task(cor1)
    task2 = asyncio.create_task(cor2)

    background_tasks.add(task1)
    task1.add_done_callback(background_tasks.discard)
    background_tasks.add(task2)
    task2.add_done_callback(background_tasks.discard)

    print(datetime.now())


if __name__ == '__main__':
    print("ypa ypa ypa ypa")
    asyncio.run(main())