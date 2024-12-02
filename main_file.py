import os
import time
import csv
from keypad import read_keypad, verify_passcode, roll_list
import display
import evdev
import sys
from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
import threading
import subprocess
import queue
import cv2
import numpy as np
from picamera2 import Picamera2
from constants import STUDENT_STRENGTH, SUBJECTS, DEPT, SEM
from miscellaneous import show_data, copy_data, delete_data
import attendance
import subject_select

def main_menu():
    print("1 - STUDENT ATTENDANCE")
    print("2 - TEACHER ATTENDANCE ")
    print("3 - SHOW DATA")
    print("4 - SHUT DOWN")
    print("C - COPY DATA")
    print("D - DELETE DATA")

    while True:
        display.draw([
        "1 - ATTENDANCE",
        "2 - SELECT SUBJECT",
        "3 - SHOW DATA",
        "4 - SHUT DOWN"
        ])

        if read_keypad == "1":
            subprocess.run(['python3', 'attendance.py'])
        elif read_keypad == "2":
            subprocess.run(['python3', 'subject_select.py'])  # change to teacher attendance
        elif read_keypad == "3":
            subprocess.run(["python3", "miscellaneous.py", "show_data"])
        elif read_keypad == "4":
            print("[INFO] Exiting the program. Goodbye!")
            break
        elif read_keypad == "C":
            subprocess.run(["python3", "miscellaneous.py", "copy_data"])
        elif read_keypad == "D":
            subprocess.run(["python3", "miscellaneous.py", "delete_data"])

if __name__ == '__main__':
    main_menu()
