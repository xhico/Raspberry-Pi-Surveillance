# -*- coding: utf-8 -*-
# !/usr/bin/python3

# sudo apt-get install python3 python3-pip python3-dev python3-rpi.gpio libatlas-base-dev gpac libxslt-dev -y
# pip3 install yagmail picamera numpy

import os
import time
import subprocess
import RPi.GPIO as GPIO
from dotenv import load_dotenv
load_dotenv()

debug = False
mac_addr = os.environ.get('BLUETOOTH')


def scanXhicoS8():
    if debug:
        print("Scanning for bluetooth")

    process = subprocess.Popen(['sudo', 'l2ping', '-c', '1', mac_addr],
                               bufsize=1,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    while True:
        line = process.stdout.readlines()
        if not line:
            break
        else:
            if "Host is down" in str(line):
                return False
            else:
                return True

    return False


def stopRun():
    if debug:
        print("Stop")
    os.system("pkill -f snowden.py")
    os.system("rm -rf __pycache__/ *.h264")

    global isRunning
    isRunning = False
    return


def startRun():
    if debug:
        print("Start")

    os.system("pkill -f 'snowden.py'")
    os.system("rm -rf __pycache__/ *.h264")
    os.system("python3 snowden.py &")

    global isRunning
    isRunning = True
    return


if __name__ == '__main__':
    isRunning = False

    try:
        while True:
            isHere = scanXhicoS8()

            if debug:
                print("isHere - " + str(isHere))
            if debug:
                print("isRunning - " + str(isRunning))

            if isHere and isRunning:
                stopRun()
            elif not isHere and not isRunning:
                startRun()

            if debug:
                print("")
            time.sleep(5)

    except:
        os.system("pkill -f 'python3 snowden.py'")
        os.system("rm -rf __pycache__/ *.h264")
        GPIO.cleanup()
