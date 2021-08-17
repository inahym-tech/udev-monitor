import pyudev
import serial
import threading
import requests


def serial_threading(tty_path, post_url):
    ser = serial.Serial(tty_path)
    while ser.is_open:
        try:
            status = ser.read(2).decode('utf-8').replace('\x00', '')
            post_data = {'status': status}
            try:
                response = requests.post(post_url, json=post_data)
            except requests.exceptions.ConnectionError:
                print('connection error')
            else:
                print(response.status_code)
        except serial.serialutil.SerialException:
            ser.close()
            print(tty_path, 'is close')


if __name__ == '__main__':
    context = pyudev.Context()
    ttyList = context.list_devices(subsystem='tty', ID_VENDOR_ID='0x15ad')
    for tty in ttyList:
        ttyPath = tty.get('DEVNAME')
        print('start ', ttyPath)
        # threading.Thread(target=serial_threading(ttyPath))

    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='tty')
    monitor.start()
    for device in iter(monitor.poll, None):
        action = device.action
        if action == 'add':
            devname = device.get('DEVNAME')
            id_vendor_id = device.get('ID_VENDOR_ID')
            id_serial_short = device.get('ID_SERIAL_SHORT')
            devpath = device.get('DEVPATH')

            post_url = f'http://localhost:8000/' + id_serial_short + '/'
            post_data = {
                'DEVNAME': devname,
                'ID_VENDOR_ID': id_vendor_id,
                'ID_SERIAL_SHORT': id_serial_short,
                'DEVPATH': devpath
            }
            print(post_data)
            try:
                response = requests.post(post_url, json=post_data)
            except requests.exceptions.ConnectionError:
                print('connection error')
            else:
                print(response.status_code)

            status_post_url = f'http://localhost:8000/' + id_serial_short + '/status'
            threading.Thread(target=serial_threading(devname, status_post_url))
