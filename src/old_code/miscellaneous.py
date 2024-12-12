import os
import csv
import time
import display
from constants import SUBJECTS
from subject_select import SubjectSelect
from pyfingerprint.pyfingerprint import PyFingerprint


def show_data(fingerprint_sensor: PyFingerprint, subject: str, date: str):
    print(f'\n[SD] COUNT: {fingerprint_sensor.getTemplateCount()}')
    print(f"[SD] SUBJECT: {subject}\n")
    display.draw([f"COUNT: {fingerprint_sensor.getTemplateCount()}", f"SUBJECT: {subject}"])
    time.sleep(2)


def copy_data(subject, date):
    if not os.path.exists(f'data/{date}_{subject}.csv'):
        display.draw(["SELECTED SUBJECT FILE IS ABSENT"])
        print("\n[CD] SELECTED SUBJECT FILE IS ABSENT!")
        return

    prev_subject = subject
    subject_select = SubjectSelect()
    subject_select.subject_select()

    with open(f'data/{date}_{prev_subject}.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open(f'data/{date}_{subject}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print(f"[CD] COPIED DATA FROM {SUBJECTS[prev_subject]} to {SUBJECTS[subject]}")
    display.draw(["COPIED DATA"])
    time.sleep(1)

def delete_data(subject, date):
    if not os.path.exists(f'data/{date}_{subject}.csv'):
        display.draw(["SELECTED STUDENT FILE IS ABSENT!"])
        print("\n[DD] SELECTED STUDENT FILE IS ABSENT!")
        time.sleep(1)
        return

    absent = roll_list()

    with open(f'data/{date}_{subject}.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    filtered_rows = [row for row in rows if row[0] not in absent]

    with open(f'data/{date}_{subject}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_rows)

    display.draw(["SELECTED ROWS REMOVED"])
    print("[DD] ALL SELECTED ROLLS REMOVED")
    time.sleep(1)
