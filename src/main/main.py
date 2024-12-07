import logging
import threading
import queue
import sys

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
    currentSubjectTeacher = None

    fingerprint_class = FingerPrintAttendance()
    face_class = FaceAttendance()
    result_queue = queue.Queue()

    def fingerprint_thread():
        fingerprint_class.fingerprint_attendance(result_queue)
    def face_thread():
        face_class.face_attendance(result_queue)

    thread1 = threading.Thread(target=face_thread)
    thread2 = threading.Thread(target=fingerprint_thread)

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
            logging.info("Starting student attendance")
            if currentSubjectTeacher is None:
                logging.info("no subject selected")
                draw(["no subject", "selected"], 1)

        if read_keypad() == "2":
            logging.info("Starting teacher attendance")

            if verify_passcode():
                draw(["detecting fingerprint", "or face"])
                thread1.start()
                thread2.start()

                result_type, result_value = result_queue.get()

                thread1.join()
                thread2.join()

                if result_queue.empty():
                    logging.info("timeout")
                    draw(["timeout"], 1)
                    continue
                else:
                    logging.info(f"first to finish: {result_type} with value: {result_value}")

            else:
                continue

if __name__ == '__main__':
    main_menu()