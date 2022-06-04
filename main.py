from multiprocessing import Process
from plate.plateDetecWithCamera import camera_get_plate


def camera_one():
    while 1:
        camera_get_plate('192.168.1.114:8080')


def camera_two():
    while 1:
        # camera_get_plate(0)
        a = 8


if __name__ == '__main__':

    thread_one = Process(target=camera_one)
    thread_one.start()

    thread_two = Process(target=camera_two)
    thread_two.start()
