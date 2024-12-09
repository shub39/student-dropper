import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class Student:
    """Class to hold student data"""
    def __init__(self, index, roll, name):
        self.index = index
        self.roll = roll,
        self.name = name

    def __str__(self):
        return f"Student(index={self.index}, roll={self.roll}, name={self.name})"

class Teacher:
    """Class to hold teacher data"""
    def __init__(self, index, roll, name, subject):
        self.index = index
        self.roll = roll
        self.name = name
        self.subject = subject

    def __str__(self):
        return f"Teacher(index={self.index}, roll={self.roll}, name={self.name}, subject={self.subject})"

def load_students():
    """Loads students from studentdata.csv"""
    students = []

    try:
        with open("studentdata.csv", "r") as file1:
            reader = csv.reader(file1)

            for line in reader:
                student = Student(
                    index = str(line[0]),
                    roll = str(int(line[1])),
                    name = str(line[2])
                )
                students.append(student)
                logging.info("Added Student: " + student.__str__())
    except Exception as e:
        logging.error("Cant load students.", e)
        return students

    return students

def load_teachers():
    """Loads teachers from teacherdata.csv"""
    teachers = []

    try:
        with open("teacherdata.csv", "r") as file1:
            reader = csv.reader(file1)

            for line in reader:
                teacher = Teacher(
                    index = str(line[0]),
                    roll = str(line[1]),
                    name = str(line[2]),
                    subject = str(line[3])
                )
                teachers.append(teacher)
                logging.info("Added teacher: " + teacher.__str__())
    except Exception as e:
        logging.error("Cant load teachers: ", e)
        return teachers

    return teachers