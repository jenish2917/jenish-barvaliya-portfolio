// C# Basics Assignment
// Simple C# program to demonstrate basic concepts

using System;
using System.Collections.Generic;

public class CSharpBasicsAssignment 
{
    // Main method - starting point of the program
    public static void Main(string[] args) 
    {
        Console.WriteLine("C# Basics Assignment");
        Console.WriteLine("====================");
        
        // 1. Variables and data types
        Console.WriteLine("\n1. Variables and Data Types:");
        
        // Different types of variables
        string name = "John";
        int age = 25;
        double height = 5.8;
        bool isStudent = true;
        
        Console.WriteLine("Name: " + name);
        Console.WriteLine("Age: " + age);
        Console.WriteLine("Height: " + height);
        Console.WriteLine("Is Student: " + isStudent);
        
        // 2. Operators
        Console.WriteLine("\n2. Operators:");
        
        int a = 15;
        int b = 4;
        
        // Arithmetic operations
        int sum = a + b;
        int difference = a - b;
        int product = a * b;
        int quotient = a / b;
        int remainder = a % b;
        
        Console.WriteLine("With a=" + a + " and b=" + b + ":");
        Console.WriteLine("Addition: " + sum);
        Console.WriteLine("Subtraction: " + difference);
        Console.WriteLine("Multiplication: " + product);
        Console.WriteLine("Division: " + quotient);
        Console.WriteLine("Remainder: " + remainder);
        
        // Comparison operations
        bool isEqual = (a == b);
        bool isGreater = (a > b);
        Console.WriteLine("Are they equal? " + isEqual);
        Console.WriteLine("Is a greater than b? " + isGreater);
        
        // 3. Loops
        Console.WriteLine("\n3. Loops:");
        
        // For loop
        Console.WriteLine("For loop (0 to 4):");
        for(int i = 0; i < 5; i++) 
        {
            Console.WriteLine("  " + i);
        }
        
        // While loop
        Console.WriteLine("While loop counting down from 5:");
        int count = 5;
        while(count > 0) 
        {
            Console.WriteLine("  " + count);
            count = count - 1;
        }
        
        // 4. Arrays
        Console.WriteLine("\n4. Arrays:");
        
        // Creating an array
        int[] numbers = {1, 2, 3, 4, 5};
        Console.WriteLine("Numbers array: [" + string.Join(", ", numbers) + "]");
        
        // Accessing array elements
        Console.WriteLine("First element: " + numbers[0]);
        Console.WriteLine("Last element: " + numbers[4]);
        
        // Loop through array
        Console.WriteLine("All elements:");
        for(int i = 0; i < numbers.Length; i++) 
        {
            Console.WriteLine("  " + numbers[i]);
        }
        
        // 5. Static method example
        Console.WriteLine("\n5. Static Method:");
        
        int result = AddNumbers(10, 20);
        Console.WriteLine("Result of adding 10 and 20: " + result);
        
        // 6. Strings
        Console.WriteLine("\n6. Strings:");
        
        string text = "Hello, C# World!";
        Console.WriteLine("Original text: " + text);
        
        // String operations
        string upperText = text.ToUpper();
        string lowerText = text.ToLower();
        int textLength = text.Length;
        
        Console.WriteLine("Uppercase: " + upperText);
        Console.WriteLine("Lowercase: " + lowerText);
        Console.WriteLine("Length: " + textLength);
        
        // String concatenation
        string greeting = "Hello, ";
        string person = "Alice";
        string fullGreeting = greeting + person + "!";
        Console.WriteLine("Greeting: " + fullGreeting);
        
        // 7. Inheritance example
        Console.WriteLine("\n7. Inheritance:");
        
        // Create a dog object
        Dog myDog = new Dog("Buddy", "Golden Retriever");
        Console.WriteLine(myDog.GetInfo());
        Console.WriteLine("Sound: " + myDog.MakeSound());
        
        // Create a cat object
        Cat myCat = new Cat("Whiskers", "Orange");
        Console.WriteLine(myCat.GetInfo());
        Console.WriteLine("Sound: " + myCat.MakeSound());
        
        // 8. Access modifiers example
        Console.WriteLine("\n8. Access Modifiers:");
        
        Person person1 = new Person("John", 25, "123-45-6789");
        Console.WriteLine("Name: " + person1.GetName());  // Public
        Console.WriteLine("Age: " + person1.GetAge());    // Protected (accessible)
        // Console.WriteLine(person1.ssn);  // Private - not accessible directly
        
        // 9. Abstract class example
        Console.WriteLine("\n9. Abstract Classes:");
        
        Shape rectangle = new Rectangle(5, 3);
        Shape circle = new Circle(4);
        
        Console.WriteLine("Rectangle area: " + rectangle.CalculateArea());
        Console.WriteLine("Rectangle perimeter: " + rectangle.CalculatePerimeter());
        Console.WriteLine("Circle area: " + Math.Round(circle.CalculateArea(), 2));
        Console.WriteLine("Circle perimeter: " + Math.Round(circle.CalculatePerimeter(), 2));
        
        // 10. Exception handling
        Console.WriteLine("\n10. Exception Handling:");
        
        SafeDivide(10, 2);
        SafeDivide(10, 0);
        
        // 11. Collections
        Console.WriteLine("\n11. Collections:");
        
        List<string> fruits = new List<string>();
        fruits.Add("apple");
        fruits.Add("banana");
        fruits.Add("orange");
        
        Console.WriteLine("Fruits list: [" + string.Join(", ", fruits) + "]");
        Console.WriteLine("Number of fruits: " + fruits.Count);
        
        // Add more fruits
        fruits.Add("grape");
        Console.WriteLine("After adding grape: [" + string.Join(", ", fruits) + "]");
        
        // Check if contains
        bool hasApple = fruits.Contains("apple");
        Console.WriteLine("Has apple? " + hasApple);
        
        // 12. Constructor example
        Console.WriteLine("\n12. Constructors:");
        
        Student student1 = new Student("Alice", 20, "Computer Science");
        Student student2 = new Student("Bob", 19);
        
        Console.WriteLine(student1.GetStudentInfo());
        Console.WriteLine(student2.GetStudentInfo());
        
        Console.WriteLine("\nC# assignment completed successfully!");
    }
    
    // Static method to add two numbers
    public static int AddNumbers(int x, int y) 
    {
        return x + y;
    }
    
    // Method to safely divide two numbers
    public static void SafeDivide(int numerator, int denominator) 
    {
        try 
        {
            int result = numerator / denominator;
            Console.WriteLine(numerator + " divided by " + denominator + " = " + result);
        } 
        catch(DivideByZeroException e) 
        {
            Console.WriteLine("Error: Cannot divide by zero!");
        }
    }
}

// Parent class for inheritance example
class Animal 
{
    protected string name;
    protected string species;
    
    public Animal(string name, string species) 
    {
        this.name = name;
        this.species = species;
    }
    
    public virtual string GetInfo() 
    {
        return name + " is a " + species;
    }
    
    public virtual string MakeSound() 
    {
        return "Some sound";
    }
}

// Child class extending Animal
class Dog : Animal 
{
    private string breed;
    
    public Dog(string name, string breed) : base(name, "Dog")  // Call parent constructor
    {
        this.breed = breed;
    }
    
    public override string GetInfo() 
    {
        return name + " is a " + breed + " " + species;
    }
    
    public override string MakeSound() 
    {
        return "Woof!";
    }
}

// Another child class
class Cat : Animal 
{
    private string color;
    
    public Cat(string name, string color) : base(name, "Cat")
    {
        this.color = color;
    }
    
    public override string GetInfo() 
    {
        return name + " is a " + color + " " + species;
    }
    
    public override string MakeSound() 
    {
        return "Meow!";
    }
}

// Class to demonstrate access modifiers
class Person 
{
    public string name;        // Public - can be accessed from anywhere
    protected int age;         // Protected - accessible in same package and subclasses
    private string ssn;        // Private - only accessible within this class
    
    public Person(string name, int age, string ssn) 
    {
        this.name = name;
        this.age = age;
        this.ssn = ssn;
    }
    
    // Public methods to access private data
    public string GetName() 
    {
        return name;
    }
    
    public int GetAge() 
    {
        return age;
    }
    
    public string GetSSN() 
    {
        return ssn;
    }
}

// Abstract class example
abstract class Shape 
{
    protected string name;
    
    public Shape(string name) 
    {
        this.name = name;
    }
    
    // Abstract methods - must be implemented by subclasses
    public abstract double CalculateArea();
    public abstract double CalculatePerimeter();
}

// Rectangle class extending Shape
class Rectangle : Shape 
{
    private double width;
    private double height;
    
    public Rectangle(double width, double height) : base("Rectangle")
    {
        this.width = width;
        this.height = height;
    }
    
    public override double CalculateArea() 
    {
        return width * height;
    }
    
    public override double CalculatePerimeter() 
    {
        return 2 * (width + height);
    }
}

// Circle class extending Shape
class Circle : Shape 
{
    private double radius;
    
    public Circle(double radius) : base("Circle")
    {
        this.radius = radius;
    }
    
    public override double CalculateArea() 
    {
        return Math.PI * radius * radius;
    }
    
    public override double CalculatePerimeter() 
    {
        return 2 * Math.PI * radius;
    }
}

// Student class with constructors
class Student 
{
    private string name;
    private int age;
    private string major;
    
    // Constructor with all parameters
    public Student(string name, int age, string major) 
    {
        this.name = name;
        this.age = age;
        this.major = major;
    }
    
    // Constructor with just name and age (major defaults to "Undeclared")
    public Student(string name, int age) 
    {
        this.name = name;
        this.age = age;
        this.major = "Undeclared";
    }
    
    public string GetStudentInfo() 
    {
        return name + ", age " + age + ", major: " + major;
    }
}