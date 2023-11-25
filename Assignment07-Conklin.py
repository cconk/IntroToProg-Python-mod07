# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: Demonstrates using data classes with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Chad Conklin, 11/13/2023,Modified for Assignment07 requirements
# ------------------------------------------------------------------------------------------ #
import json

# Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Data Variables
students: list = []  # Table of student data
menu_choice: str = ""  # User's menu choice

# Data Classes
class Person:
    """ Represents a person """
    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value.isalpha():
            raise ValueError("First name must contain only letters")
        self._first_name = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value.isalpha():
            raise ValueError("Last name must contain only letters")
        self._last_name = value

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Student(Person):
    """ Represents a student, inheriting from Person """
    def __init__(self, first_name: str, last_name: str, course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self, value: str):
        self._course_name = value

    def __str__(self) -> str:
        return f"{super().__str__()} enrolled in {self.course_name}"

# Processing Class
class FileProcessor:
    """ Processes data to and from a file """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        try:
            with open(file_name, "r") as file:
                student_data.clear()
                student_data.extend([Student(**item) for item in json.load(file)])
        except FileNotFoundError as e:
            IO.output_error_messages("File not found, creating a new file.", e)
            FileProcessor.write_data_to_file(file_name, student_data)
        except Exception as e:
            IO.output_error_messages("An error occurred while reading the file.", e)

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        try:
            with open(file_name, "w") as file:
                json.dump([student.__dict__ for student in student_data], file)
                IO.output_student_and_course_names(student_data)
        except Exception as e:
            IO.output_error_messages("An error occurred while writing to the file.", e)

# Presentation Class
class IO:
    """ Handles input and output operations """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message)
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        print(menu)

    @staticmethod
    def input_menu_choice() -> str:
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages("Invalid menu choice.", e)
            return ""
        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        print("-" * 50)
        for student in student_data:
            print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data() -> Student:
        try:
            first_name = input("Enter the student's first name: ")
            last_name = input("Enter the student's last name: ")
            course_name = input("Enter the course name: ")
            return Student(first_name, last)
        except ValueError as e:
            IO.output_error_messages("Invalid input.", e)
            return None

# Main Body of Script
students = FileProcessor.read_data_from_file(FILE_NAME, students)

while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        student = IO.input_student_data()
        if student:
            students.append(student)

    elif menu_choice == "2":
        IO.output_student_and_course_names(students)

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)

    elif menu_choice == "4":
        break

print("Program Ended")