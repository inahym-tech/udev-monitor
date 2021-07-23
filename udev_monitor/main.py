import asyncio
import pyudev
import serial


def main(_, tty):
    ttyPath = tty.get('DEVNAME')
    s = serial.Serial(ttyPath)
    while True:
        print(ttyPath, s.read(2)[:1])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.futures.Future()
    context = pyudev.Context()
    ttyList = context.list_devices(subsystem='tty', ID_VENDOR_ID='0x15ad')
    for tty in ttyList:
        loop.call_soon(main, future, tty)
    res = loop.run_forever()
