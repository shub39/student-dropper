import os
import shutil
import csv
from pyfingerprint.pyfingerprint import PyFingerprint
from time import sleep

def clear_database(fingerprint_port='/dev/ttyUSB0'):
    try:
        f = PyFingerprint(fingerprint_port, 57600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        print(f"[ERROR] Unable to connect to fingerprint sensor: {e}")
        return

    for i in range(f.getTemplateCount()):
        f.deleteTemplate(i)
    with open('studentdata.csv', 'w') as file:
        file.close()
    shutil.rmtree("old_dataset")
    shutil.rmtree("dataset")
    print("[INFO] ALL DATA CLEARED\n")
    sleep(2)
