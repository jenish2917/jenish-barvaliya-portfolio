# JALA Academy - Python Basics Assignments

print("Python Basics - Assignment Solutions")
print("====================================")

# 1. Python Basics
print("\n1. Variables and Data Types:")

# Just learning basic variables
name = "John"
age = 25
height = 5.8
is_student = True

type_name = type(name)
type_age = type(age)
type_height = type(height)
type_student = type(is_student)

print(f"Name: {name}, Type: {type_name}")
print(f"Age: {age}, Type: {type_age}")
print(f"Height: {height}, Type: {type_height}")
print(f"Is Student: {is_student}, Type: {type_student}")

# Simple input/output
temp_name = "Alice"  # Using default instead of input for now
print(f"Hello, {temp_name}!")

# 2. Operators
print("\n2. Operators:")

a = 15
b = 4

# Arithmetic operations
add_result = a + b
sub_result = a - b
mul_result = a * b
div_result = a / b
floor_div_result = a // b
mod_result = a % b
exp_result = a ** b

print(f"With a={a} and b={b}:")
print(f"Addition: {add_result}")
print(f"Subtraction: {sub_result}")
print(f"Multiplication: {mul_result}")
print(f"Division: {div_result}")
print(f"Floor Division: {floor_div_result}")
print(f"Modulus: {mod_result}")
print(f"Exponent: {exp_result}")

# Comparison operations
equal_check = a == b
not_equal_check = a != b
greater_check = a > b
less_check = a < b
greater_equal_check = a >= b
less_equal_check = a <= b

print(f"\nComparison Results:")
print(f"Equal: {equal_check}")
print(f"Not Equal: {not_equal_check}")
print(f"Greater: {greater_check}")
print(f"Less: {less_check}")
print(f"Greater or Equal: {greater_equal_check}")
print(f"Less or Equal: {less_equal_check}")

# Logical operations
x = True
y = False

and_result = x and y
or_result = x or y
not_result = not x

print(f"\nLogical Operations:")
print(f"AND: {and_result}")
print(f"OR: {or_result}")
print(f"NOT: {not_result}")

# 3. Loops
print("\n3. Loops:")

print("For loop counting 0 to 4:")
for i in range(5):
    print(f"  {i}")

print("\nWhile loop counting down from 5:")
count = 5
while count > 0:
    print(f"  {count}")
    count = count - 1

print("\nLoop with break and continue:")
for i in range(10):
    if i == 3:
        continue  # Skip number 3
    if i == 7:
        break     # Stop when reach 7
    print(f"  {i}")

print()

# 4. Lists (Arrays)
print("\n4. Lists (Arrays):")

# Creating and accessing lists
numbers = [1, 2, 3, 4, 5]
print(f"Original list: {numbers}")
print(f"First element: {numbers[0]}")
print(f"Last element: {numbers[-1]}")

# List operations
numbers.append(6)
print(f"After adding 6: {numbers}")

numbers.insert(2, 10)  # Insert 10 at position 2
print(f"After inserting 10 at position 2: {numbers}")

numbers.remove(10)  # Remove the number 10
print(f"After removing 10: {numbers}")

# List slicing
slice1 = numbers[1:4]
slice2 = numbers[:3]
slice3 = numbers[2:]
print(f"Slice [1:4]: {slice1}")
print(f"Slice [:3]: {slice2}")
print(f"Slice [2:]: {slice3}")

# Making a list of squares
squares = []
for x in range(1, 6):
    squares.append(x**2)
print(f"Squares from 1 to 5: {squares}")

print()

# 5. Static methods
print("\n5. Static Methods:")

# Simple functions instead of static methods
def add_numbers(x, y):
    return x + y

def multiply_numbers(x, y):
    return x * y

result_add = add_numbers(5, 3)
result_multiply = multiply_numbers(4, 6)
print(f"Add function result: {result_add}")
print(f"Multiply function result: {result_multiply}")

print()

# 6. Strings
print("\n6. Strings:")

text = "Hello, Python World!"
print(f"Original string: {text}")

# String operations
upper_text = text.upper()
lower_text = text.lower()
title_text = text.title()
replaced_text = text.replace('Python', 'Java')
split_text = text.split(',')
text_length = len(text)

print(f"Uppercase: {upper_text}")
print(f"Lowercase: {lower_text}")
print(f"Title case: {title_text}")
print(f"Replace 'Python' with 'Java': {replaced_text}")
print(f"Split by comma: {split_text}")
print(f"Length: {text_length}")

# String formatting
name = "Alice"
age = 30
formatted_str = f"My name is {name} and I am {age} years old."
print(f"Formatted string: {formatted_str}")

# String slicing
slice1 = text[0:5]
slice2 = text[7:]
print(f"Substring [0:5]: {slice1}")
print(f"Substring [7:]: {slice2}")

print()

# 7. Inheritance
print("\n7. Inheritance:")

# Creating a parent class
# I'm making a simple animal class first
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some sound"
    
    def get_info(self):
        return f"{self.name} is a {self.species}"

# Creating a child class
# Dog inherits from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        # Call parent constructor
        super().__init__(name, "Dog")
        self.breed = breed
    
    def make_sound(self):
        return "Woof!"
    
    def get_info(self):
        return f"{self.name} is a {self.breed} {self.species}"

# Another child class
class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color
    
    def make_sound(self):
        return "Meow!"

# Using the classes
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers", "Orange")

print(f"Dog: {dog.get_info()}")
print(f"Dog sound: {dog.make_sound()}")
print(f"Cat: {cat.get_info()}")
print(f"Cat color: {cat.color}")
print(f"Cat sound: {cat.make_sound()}")

print()

# 8. Access Modifiers
print("\n8. Access Modifiers:")

class Person:
    def __init__(self, name, age, ssn):
        # Public - anyone can access
        self.name = name
        # Protected - should be accessed within class and subclasses
        self._age = age  
        # Private - should only be accessed within this class
        self.__ssn = ssn  
    
    def get_private_info(self):
        # Method to access private info safely
        return self.__ssn

person = Person("John", 25, "123-45-6789")

print(f"Name (public): {person.name}")
print(f"Age (protected): {person._age}")
print(f"SSN (private via method): {person.get_private_info()}")

print()

# 9. Abstract Classes
print("\n9. Abstract Classes:")

# For this example, I'll create classes without using ABC
# since it's more advanced

class Shape:
    def __init__(self, name):
        self.name = name
    
    def area(self):
        # This should be implemented by child classes
        raise NotImplementedError("Subclass must implement area method")
    
    def perimeter(self):
        # This should be implemented by child classes
        raise NotImplementedError("Subclass must implement perimeter method")

# Rectangle class
class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Circle class
class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        return 3.14159 * (self.radius ** 2)
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Using the shapes
rectangle = Rectangle(5, 3)
circle = Circle(4)

print(f"Rectangle area: {rectangle.area()}")
print(f"Rectangle perimeter: {rectangle.perimeter()}")
print(f"Circle area: {circle.area():.2f}")
print(f"Circle perimeter: {circle.perimeter():.2f}")

print()

# 10. Multiple Inheritance
print("\n10. Multiple Inheritance:")

# Simple example without abstract classes
class Drawable:
    def __init__(self):
        self.is_drawn = False
    
    def draw(self):
        self.is_drawn = True
        return f"Drawing the {self.__class__.__name__}"

class Resizable:
    def __init__(self):
        self.size = 1
    
    def resize(self, factor):
        self.size *= factor
        return f"Resized by factor {factor}, new size: {self.size}"

# Square class inheriting from both
class Square(Drawable, Resizable):
    def __init__(self, side):
        # Call both parent constructors
        Drawable.__init__(self)
        Resizable.__init__(self)
        self.side = side
    
    def get_info(self):
        return f"Square with side {self.side}"

square = Square(5)
print(square.draw())
print(square.resize(2))
print(square.get_info())

print()

# 11. Self and Super
print("\n11. Self and Super:")

# Parent class
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        print(f"Vehicle created: {self.brand} {self.model}")
    
    def start(self):
        return f"{self.brand} {self.model} is starting"

# Child class
class Car(Vehicle):
    def __init__(self, brand, model, doors):
        # Call parent constructor using super
        super().__init__(brand, model)
        self.doors = doors
        print(f"Car has {self.doors} doors")
    
    def start(self):
        # Call parent method using super
        parent_result = super().start()
        return f"{parent_result} with {self.doors} doors"

my_car = Car("Toyota", "Camry", 4)
print(my_car.start())

print()

# 12. Constructors
print("\n12. Constructors:")

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.grade = "Not Set"
        print(f"New student created: {self.name}, age {self.age}")
    
    def set_grade(self, grade):
        self.grade = grade
    
    def get_info(self):
        return f"{self.name}, age {self.age}, grade: {self.grade}"

# Creating student objects
student1 = Student("John", 20)
student2 = Student("Mary", 19)

# Setting grades
student1.set_grade("A")
student2.set_grade("B+")

print(student1.get_info())
print(student2.get_info())

print()

# 13. Function Overloading (using default parameters)
print("\n13. Function Parameters:")

# Python doesn't support method overloading like Java
# But we can achieve similar results with default parameters

def calculate_area(length, width=None):
    if width is None:
        # If only one parameter, calculate area of square
        return length * length
    else:
        # If two parameters, calculate area of rectangle
        return length * width

# Testing the function
square_area = calculate_area(5)
rectangle_area = calculate_area(5, 3)

print(f"Area of square with side 5: {square_area}")
print(f"Area of rectangle 5x3: {rectangle_area}")

# Using *args for variable number of arguments
def add_numbers(*args):
    total = 0
    for num in args:
        total += num
    return total

result1 = add_numbers(1, 2)
result2 = add_numbers(1, 2, 3, 4)
result3 = add_numbers(10, 20, 30, 40, 50)

print(f"Adding 2 numbers: {result1}")
print(f"Adding 4 numbers: {result2}")
print(f"Adding 5 numbers: {result3}")

print()

# 14. Exceptions
print("\n14. Exceptions:")

# Simple division function with exception handling
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Can't divide by zero!")
        return "Error"
    except TypeError:
        print("Error: Please use numbers only!")
        return "Error"

# Testing division
print(f"10 divided by 2: {safe_divide(10, 2)}")
print(f"10 divided by 0: {safe_divide(10, 0)}")
print(f"10 divided by 'a': {safe_divide(10, 'a')}")

# Handling list index errors
def get_list_item(my_list, index):
    try:
        item = my_list[index]
        return item
    except IndexError:
        print(f"Error: Index {index} is out of range")
        return None

numbers = [10, 20, 30]
print(f"Item at index 1: {get_list_item(numbers, 1)}")
print(f"Item at index 5: {get_list_item(numbers, 5)}")

print()

# 15. File I/O
print("\n15. File Input/Output:")

# Writing to a file
filename = "student_data.txt"

# Writing data to file
with open(filename, 'w') as file:
    file.write("Student Name: John Doe\n")
    file.write("Age: 20\n")
    file.write("Grade: A\n")

print(f"Data written to {filename}")

# Reading the entire file
with open(filename, 'r') as file:
    content = file.read()
    print(f"\nContent of {filename}:")
    print(content)

# Reading line by line
with open(filename, 'r') as file:
    print("Reading line by line:")
    line1 = file.readline()
    line2 = file.readline()
    line3 = file.readline()
    print(f"Line 1: {line1.strip()}")
    print(f"Line 2: {line2.strip()}")
    print(f"Line 3: {line3.strip()}")

# Appending to file
with open(filename, 'a') as file:
    file.write("Subject: Computer Science\n")

print(f"\nAfter appending new line:")
with open(filename, 'r') as file:
    print(file.read())

# Clean up the file
import os
os.remove(filename)
print(f"File {filename} has been removed")

print()

# 16. Collections
print("\n16. Collections:")

# Lists
fruits = ["apple", "banana", "orange", "apple"]
print(f"Fruits list: {fruits}")

# Count occurrences
apple_count = fruits.count("apple")
print(f"Number of apples: {apple_count}")

# Add to list
fruits.append("grape")
print(f"After adding grape: {fruits}")

# Tuples (unchangeable)
coordinates = (10, 20, 30)
print(f"\nCoordinates tuple: {coordinates}")
print(f"First coordinate: {coordinates[0]}")

# Sets (no duplicates)
unique_numbers = {1, 2, 3, 4, 5, 3, 2}  # duplicate 3 and 2 will be removed
print(f"\nUnique numbers set: {unique_numbers}")

# Add to set
unique_numbers.add(6)
print(f"After adding 6: {unique_numbers}")

# Remove from set
unique_numbers.discard(3)
print(f"After removing 3: {unique_numbers}")

# Dictionaries
student = {
    "name": "Alice",
    "age": 22,
    "grade": "A"
}
print(f"\nStudent dictionary: {student}")
print(f"Student name: {student['name']}")

# Add new key-value pair
student["major"] = "Computer Science"
print(f"After adding major: {student}")

# Update existing value
student["age"] = 23
print(f"After updating age: {student}")

print()

# 17. Importing modules
print("\n17. Using Built-in Modules:")

import math
import random

# Using math module
number = 16
sqrt_result = math.sqrt(number)
pi_value = math.pi

print(f"Square root of {number}: {sqrt_result}")
print(f"Value of pi: {pi_value:.2f}")

# Using random module
random_num = random.randint(1, 10)
print(f"Random number between 1 and 10: {random_num}")

# More random examples
random_choice = random.choice(["apple", "banana", "orange"])
print(f"Random choice from list: {random_choice}")

# 18. Dictionary operations
print("\n18. Dictionary Operations:")

# Creating a dictionary
student_grades = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "Diana": 96
}

print(f"Student grades: {student_grades}")

# Getting keys and values
names = list(student_grades.keys())
grades = list(student_grades.values())

print(f"Student names: {names}")
print(f"Grades only: {grades}")

# Adding new students
student_grades["Eve"] = 88
student_grades["Frank"] = 91

print(f"\nAfter adding more students: {student_grades}")

# Finding students with high grades
high_scorers = []
for name, grade in student_grades.items():
    if grade >= 90:
        high_scorers.append(name)

print(f"Students with grades 90 or above: {high_scorers}")

# Nested dictionary example
school = {
    "class_10A": {
        "students": ["Alice", "Bob", "Charlie"],
        "teacher": "Mr. Johnson",
        "room": 101
    },
    "class_10B": {
        "students": ["Diana", "Eve", "Frank"],
        "teacher": "Ms. Smith",
        "room": 102
    }
}

print(f"\nSchool information: {school}")
print(f"Teacher of class 10A: {school['class_10A']['teacher']}")
print(f"Students in class 10B: {school['class_10B']['students']}")

print("\nAll Python basics assignments completed successfully!")