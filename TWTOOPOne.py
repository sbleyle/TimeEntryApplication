
class Dog:

    # this method is called whenever we right Dog()
    def __init__(self, name, age):
        #attribute of class Dog()
        self.name = name
        self.age = age


    #method is function inside a class
    def add_1(self, x):
        return x + 1
    def bark(self):
        print("bark")

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

#d = Dog("Tim", 34)
#d.set_age(23)
#print(d.get_age())

class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade #0 - 100

    def get_grade(self):
        return self.grade

class Course:
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = []
        self.is_active = False

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False

    def get_average_grade(self):
        value = 0
        for student in self.students:
            value += student.get_grade()

        return value / len(self.students)

#s1 = Student("Tim", 19, 95)
#s2 = Student("Bill", 19, 75)
#s3 = Student("Jill", 19, 65)

#course = Course("Science", 2)
#course.add_student(s1)
#course.add_student(s2)
#print(course.add_student(s2))
#print(course.get_average_grade())

########################################################################
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old.")

    def speak(self):
        print("I don't know what I want to say.")

class Cat(Pet):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def speak(self):
        print("Meow")

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old and I am {self.color}.")

class Dog(Pet):
    def speak(self):
        print("Bark")

class Fish(Pet):
    pass

#p = Pet("Tim", 19)
#p.speak()
#c = Cat("Bill", 34, "Blue")
#c.show()
#d = Dog("Jill", 25)
#d.speak()
#f = Fish("Bubbles", 10)
#f.speak()
###################################################

class Person:
    number_of_people = 0

    def __init__(self, name):
        self.name = name
        Person.number_of_people += 1

p1 = Person("Tim")
print(Person.number_of_people)
p2 = Person("Jill")
print(Person.number_of_people)


#common to organize functions in classes to help with structure. This is the static method

class Math:
    @staticmethod
    def add5(x):
        return x + 5

print(Math.add5(5))