import RPi.GPIO as GPIO
import logging

from time import sleep

from display import draw
from constants import PASSCODE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Constants to read keypad
L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_keypad():
    """Reads singular input"""
    keys = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
    ]

    lines = [L1, L2, L3, L4]
    columns = [C1, C2, C3, C4]
    output = ""

    for i, line in enumerate(lines):
        GPIO.output(line, GPIO.HIGH)
        for j, column in enumerate(columns):
            if GPIO.input(column) == 1:
                output = keys[i][j]
        GPIO.output(line, GPIO.LOW)

    return output

def enter_passcode():
    """Takes 4 digit passcode"""
    input_code = ""
    draw(["ENTER PASSCODE"])
    logging.info("Enter the 4 digit passcode")

    while len(input_code) < 4:
        key = None
        while not key:
            key = read_keypad()
            sleep(0.3)

        if key:
            logging.info(f"Key pressed: {key}")
            if key.isdigit():
                input_code += key
                draw(["ENTER PASSCODE", f"{input_code}"])
                logging.info(f"Current info: {input_code}")
            elif key == "*":
                draw(["Input Reset"])
                input_code = ""
                logging.info("input Reset")

    return input_code

def enter_roll():
    """Takes 2 digit roll"""
    number = ""
    draw(["ENTER ROLL"])
    print("Enter Roll")

    while len(number) < 2:
        key = None
        while not key:
            key = read_keypad()
            sleep(0.2)

        if key:
            if key.isdigit():
                number += key
                draw(["Enter Roll", f"{number}"])
                logging.info(f"Current number: {number}")
            elif key == "*":
                number = ""
                draw(["Number reset"])
                logging.info("Number reset")

    return number

def roll_list():
    """Returns roll list"""
    numbers_list = []

    while True:
        two_digit_number = enter_roll()
        logging.info(f"Roll added: {two_digit_number}")

        while True:
            draw(["press 'A' to add roll", "press 'B' to finish", str(numbers_list)])
            logging.info("Press A to add another roll, B to finish")

            choice = None
            while not choice:
                choice = read_keypad()

            if choice == "A":
                logging.info("Adding another roll")
                break
            elif choice == "B":
                logging.info("Finished adding roll")
                return numbers_list
            else:
                continue

def verify_passcode():
    """Verifies passcode, do I have to document everything?"""
    entered_code = enter_passcode()

    if entered_code == PASSCODE:
        draw(["access granted"])
        logging.info("access granted")
        sleep(1)
        return True
    else:
        draw(["access denied"])
        logging.info("access denied")
        sleep(1)
        return False