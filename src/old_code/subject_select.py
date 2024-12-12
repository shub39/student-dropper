import display
from keypad import read_keypad, verify_passcode
from constants import SUBJECTS
import time

subject =  ""

class SubjectSelect:
    def __init__(self):
        self.subject = ""

    def subject_select(self):
        if not verify_passcode(): return

        display.draw(["SELECT SUBJECT"])
        print("\n[S] SELECT SUBJECT")

        keys = list(SUBJECTS.keys())
        for idx, key in enumerate(keys, start=1):
            print(f"{idx} : {SUBJECTS[key]}")
        
        time.sleep(1)

        while True:
            selected_key = read_keypad()

            try:
                selected_index = int(selected_key) - 1
                if 0 <= selected_index < len(SUBJECTS):
                    self.subject = keys[selected_index]
                    break
            except ValueError:
                continue

            time.sleep(0.1)

        print(f"[S] SELECTED {self.subject}: {SUBJECTS[self.subject]}")
        display.draw(["SELECTED SUBJECT", self.subject])
        time.sleep(1)
