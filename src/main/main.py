import logging
import sys

from entities import Student, Teacher, load_students, load_teachers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def main_menu():
    """Main menu of the program"""
    logging.info("Starting program")

    students = load_students()
    teachers = load_teachers()

    if len(students) == 0 or len(teachers) == 0:
        logging.error("No teachers or students enrolled")
        sys.exit(1)
    else:
        logging.info("Students loaded: " + str(len(students)))
        logging.info("Teachers loaded: " + str(len(teachers)))


if __name__ == '__main__':
    main_menu()