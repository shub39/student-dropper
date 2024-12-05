import logging
import sys

from entities import Student, Teacher, load_students, load_teachers
from keypad import read_keypad, enter_passcode, enter_roll, roll_list, verify_passcode
from display import draw

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

main_menu_items = [
    "1: STUDENT ATTENDANCE",
    "2: TEACHER ATTENDANCE",
]

def main_menu():
    """Main menu of the program"""
    logging.info("Starting program")

    # Try to load all entities into classes and exit if empty
    students = load_students()
    teachers = load_teachers()

    if len(students) == 0 or len(teachers) == 0:
        logging.error("No teachers or students enrolled")
        sys.exit(1)
    else:
        logging.info("Students loaded: " + str(len(students)))
        logging.info("Teachers loaded: " + str(len(teachers)))

    while True:
        draw(main_menu_items)

        if read_keypad() == "1":
            logging.info("Starting student attendance")
            verify_passcode()
        if read_keypad() == "2":
            logging.info("Starting teacher attendance")
            verify_passcode()

if __name__ == '__main__':
    main_menu()