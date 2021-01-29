# -*- coding: utf-8 -*-
# !/usr/bin/python3

from snowden import REC_WIDTH, REC_HEIGHT, REC_ROTATION, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER
from picamera import PiCamera
import yagmail
import time
import os


def send_mail(pic):
    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
    yag.send(EMAIL_RECEIVER, "NSA - " + pic, "", pic)
    yag.close()


def takePic(file):
    camera = PiCamera()
    camera.resolution = (REC_WIDTH, REC_HEIGHT)
    camera.rotation = REC_ROTATION
    camera.start_preview()
    time.sleep(5)
    camera.capture(file)
    camera.stop_preview()
    camera.close()


def main():
    print("Kill NSA")
    os.system("pkill -f 'python3 nsa.py'")
    os.system("pkill -f 'python3 snowden.py'")

    picFile = "pic_" + str(time.strftime('%Y-%m-%d_%H-%M-%S')) + ".jpg"

    print("TakePic")
    takePic(picFile)
    print("SendMail")
    send_mail(picFile)
    print("RemovePic")
    os.remove(picFile)

    print("Start NSA")
    os.system("python3 nsa.py &")


if __name__ == '__main__':
    main()
