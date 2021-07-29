import re
import asyncio
import pyudev
import serial_asyncio
import random


class Serial(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        print('port opened\n', transport)

    def data_received(self, data):
        print('data received', re.match('b\'(.)', str(data)).group(1))

    def connection_lost(self, exc):
        print('port closed (%s) \n' % exc)
        self.transport.close()


async def countloopTasks():
    while True:
        await asyncio.sleep(3)
        print(len([task for task in asyncio.Task.all_tasks() if not task.done()]))


async def echoHello(time):
    print('starting ', time)
    await asyncio.sleep(time)
    print('ending ', time)
    return time


async def main(loop):

    added_tasks = []
    delays = [x for x in range(10)]
    random.shuffle(delays)

    for n in delays:
        print('adding ', str(n))
        task = loop.create_task(echoHello(n))
        added_tasks.append(task)
        await asyncio.sleep(0)

    print('adding ', str(5))
    task = loop.create_task(echoHello(5))
    added_tasks.append(task)
    await asyncio.sleep(5)

    print('done adding tasks')

    running_tasks = added_tasks[::]
    while running_tasks:
        running_tasks = [x for x in running_tasks if not x.done()]
        await asyncio.sleep(0)

    print('done running tasks')

    results = [x.result() for x in added_tasks]
    return results
    #context = pyudev.Context()
    #ttyList = context.list_devices(subsystem='tty', ID_VENDOR_ID='0x15ad')
    # loop.create_task(countloopTasks())
    # for tty in ttyList:
    #    ttyPath = tty.get('DEVNAME')
    #    coro = serial_asyncio.create_serial_connection(loop, Serial, ttyPath)
    #    loop.create_task(coro)
    # loop.run_forever()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(loop))
    loop.close()
    print(results)
