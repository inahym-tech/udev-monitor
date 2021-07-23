import time
import pyudev


def main():
    filepath = "/tmp/hello.log"
    log = open(filepath, 'a')
    log.write("hello!\n")
    context = pyudev.Context()
    log.write(str(context))


if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)
