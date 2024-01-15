# Basic variable assignment
name = "John"
age = 30

# Print statement
print(f"Hello, {name}! You are {age} years old.")

# Conditional statement
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

# List and loop
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    print(number)

# Function definition
def multiply(a, b):
    return a * b

result = multiply(2, 3)
print(f"Multiplication result: {result}")

# Class and object
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

# Object instantiation
person = Person("Alice", 25)
person.introduce()

# Exception handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero.")

# File handling
with open("example.txt", "w") as file:
    file.write("This is a dummy file.")

with open("example.txt", "r") as file:
    content = file.read()
    print("File content:", content)



# Outer level
name = "John"
age = 30

if age >= 18:
    # First level of indentation
    print("You are an adult.")
    numbers = [1, 2, 3, 4, 5]

    for number in numbers:
        # Second level of indentation
        print("Outer loop:", number)

        if number % 2 == 0:
            # Third level of indentation
            print("Inner conditional: even")
        else:
            # Third level of indentation
            print("Inner conditional: odd")

    def multiply(a, b):
        # Second level of indentation within a function
        return a * b

    result = multiply(2, 3)
    print(f"Multiplication result: {result}")

else:
    # First level of indentation
    print("You are a minor.")

    class Person:
        # Second level of indentation within a class
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def introduce(self):
            # Third level of indentation within a method
            print(f"My name is {self.name} and I am {self.age} years old.")

    person = Person("Alice", 25)
    person.introduce()

    try:
        # Second level of indentation within a try block
        result = 10 / 0
    except ZeroDivisionError:
        # Third level of indentation within an except block
        print("Cannot divide by zero.")

    with open("example.txt", "w") as file:
        # Second level of indentation within a with block
        file.write("This is a dummy file.")

    with open("example.txt", "r") as file:
        # Second level of indentation within a with block
        content = file.read()
        print("File content:", content)
