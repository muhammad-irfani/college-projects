#importing class 
class Student:
    def __init__(self, name, address): 

        #initialzing the students name, and address, 
        self.__name = name
        self.__address = address
        self.__completed_courses = []
        self.__grades = []

    #applying the getter method to all four 
    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_completed_courses(self):
        return self.__completed_courses

    def get_grades(self):
        return self.__grades

    # applying the setter method to both 
    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    #assigning addition to add course and grade
    def add_course(self, course, grade):
        self.__completed_courses.append(course)
        self.__grades.append(grade)

    #assiging program to update the grade after addition 
    def update__grade(self, course, new_grade):
        if course in self.__completed_courses:
            index = self.__completed_courses.index(course)
            self.__grades[index] = new_grade
        else:
            print("Course not found.")

    #getting grade for each completed course 
    def get_grade_for_course(self, course):
        if course in self.__completed_courses:
            index = self.__completed_courses.index(course)
            return self.__grades[index]
        else:
            return None

#using information to add into dataframe 
student = Student("Muhammad Irfani", "Brooklyn Street")
student.add_course("English", 98)
student.add_course("Math", 95)

#actioning to print details and the sum of course grade  
print("Student Name:", student.get_name())
print("Address:", student.get_address())
print("Completed Courses:", student.get_completed_courses())
print("Grades:", student.get_grades())
print("Grade for English:", student.get_grade_for_course("English"))
