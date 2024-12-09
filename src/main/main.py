import csv
import logging
import os.path
import threading
import queue
import sys
import time

from entities import Student, Teacher, load_students, load_teachers
from keypad import read_keypad, enter_passcode, enter_roll, roll_list, verify_passcode
from display import draw
from fingerprint import FingerPrintAttendance
from face import FaceAttendance

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

main_menu_items = [
    "1: STUDENT",
    "2: TEACHER",
]

def main_menu():
    """Main menu of the program"""
    logging.info("Starting program")

    # global variables
    current_teacher = None

    fingerprint_class = FingerPrintAttendance()
    face_class = FaceAttendance()

    # Try to load all entities into classes and exit if empty
    students = load_students()
    teachers = load_teachers()

    if len(students) == 0 or len(teachers) == 0:
        logging.error("No teachers and/or students enrolled")
        sys.exit(1)
    else:
        logging.info("Students loaded: " + str(len(students)))
        logging.info("Teachers loaded: " + str(len(teachers)))

    while True:
        draw(main_menu_items)

        if read_keypad() == "1":
            if current_teacher is None:
                logging.info("no subject selected")
                draw(["no subject", "selected"], 1)
            else:
                student = student_attendance(fingerprint_class, face_class, students)
                if student is not None:
                    write_data(student, current_teacher)


        if read_keypad() == "2":
            current_teacher = teacher_attendance(fingerprint_class, face_class, teachers)

def write_data(student, teacher):
    time_tuple = time.localtime()
    date = time.strftime("%d-%m-%Y", time.localtime())
    time_string = time.strftime("%H:%M", time_tuple)

    if not os.path.exists('data/'):
        os.makedirs('data/')

    if not os.path.exists(f"data/{date}_{teacher.subject}.csv"):
        with open(f"data/{date}_{teacher.subject}.csv", "w") as file1:
            csvout = csv.writer(file1)
            csvout.writerow(["Roll", "Name", "Timings"])

    with open(f"data/{date}_{teacher.subject}.csv", "r") as file1:
        reader = csv.reader(file1)
        rows = list(reader)

    present = 1

    for i in rows:
        if i[1] == student.name:
            present = 0
            break

    if present == 1:
        rows.append([student.roll, student.name, time_string])

    with open(f"data/{date}_{teacher.subject}.csv", "w") as file2:
        writer = csv.writer(file2)
        writer.writerows(rows)

    logging.info("written data on " + student.name)

def student_attendance(
        fingerprint_class: FingerPrintAttendance,
        face_class: FaceAttendance,
        students
):
    """Takes students attendance"""
    logging.info("Starting student attendance")

    def fingerprint_thread():
        fingerprint_class.fingerprint_attendance(result_queue)
    def face_thread():
        face_class.face_attendance(result_queue)

    thread1 = threading.Thread(target=face_thread)
    thread2 = threading.Thread(target=fingerprint_thread)

    result_queue = queue.Queue()

    thread1.start()
    thread2.start()

    draw(["detecting fingerprint", "or face"])

    try:
        result_type, result_value = result_queue.get(timeout=5)
        logging.info(f"first to finish: {result_type} with value: {result_value}")

        if result_type == "fingerprint":
            for student in students:
                if str(result_value) == student.index:
                    logging.info("found student " + student.__str__())
                    return student
            draw(["invalid", "fingerprint"], 1)

        else:
            for student in students:
                if str(result_value) == student.roll:
                    logging.info("found student " + student.__str__())
                    return student
            draw(["invalid", "face"], 1)

    except queue.Empty:
        logging.info("timeout")
        draw(["timeout"], 1)
    finally:
        thread1.join(timeout=1)
        thread2.join(timeout=1)

def teacher_attendance(
        fingerprint_class: FingerPrintAttendance,
        face_class: FaceAttendance,
        teachers
):
    """Teacher attendance taker/ subject selector"""
    logging.info("Starting teacher attendance")

    def fingerprint_thread():
        fingerprint_class.fingerprint_attendance(result_queue)
    def face_thread():
        face_class.face_attendance(result_queue)

    thread1 = threading.Thread(target=face_thread)
    thread2 = threading.Thread(target=fingerprint_thread)

    result_queue = queue.Queue()

    if verify_passcode():
        draw(["detecting fingerprint", "or face"])
        thread1.start()
        thread2.start()

        try:
            result_type, result_value = result_queue.get(timeout=5)
            logging.info(f"first to finish: {result_type} with value: {result_value}")

            if result_type == "fingerprint":
                for teacher in teachers:
                    if str(result_value) == teacher.index:
                        draw(["subject", str(teacher.subject)], 1)
                        return teacher
                draw(["invalid", "fingerprint"], 1)
            else:
                for teacher in teachers:
                    if str(result_value - 100) == teacher.roll:
                        draw(["subject", str(teacher.subject)], 1)
                        return teacher
                draw(["invalid", "face"], 1)

        except queue.Empty:
            logging.info("timeout")
            draw(["timeout"], 1)
        finally:
            thread1.join(timeout=1)
            thread2.join(timeout=1)

if __name__ == '__main__':
    main_menu()