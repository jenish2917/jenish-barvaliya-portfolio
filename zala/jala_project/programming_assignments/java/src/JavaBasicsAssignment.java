// Java Basics Assignment
// Simple Java program to demonstrate basic concepts

public class JavaBasicsAssignment {
    
    // Main method - starting point of the program
    public static void main(String[] args) {
        System.out.println("Java Basics Assignment");
        System.out.println("======================");
        
        // 1. Variables and data types
        System.out.println("\n1. Variables and Data Types:");
        
        // Different types of variables
        String name = "John";
        int age = 25;
        double height = 5.8;
        boolean isStudent = true;
        
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Height: " + height);
        System.out.println("Is Student: " + isStudent);
        
        // 2. Operators
        System.out.println("\n2. Operators:");
        
        int a = 15;
        int b = 4;
        
        // Arithmetic operations
        int sum = a + b;
        int difference = a - b;
        int product = a * b;
        int quotient = a / b;
        int remainder = a % b;
        
        System.out.println("With a=" + a + " and b=" + b + ":");
        System.out.println("Addition: " + sum);
        System.out.println("Subtraction: " + difference);
        System.out.println("Multiplication: " + product);
        System.out.println("Division: " + quotient);
        System.out.println("Remainder: " + remainder);
        
        // Comparison operations
        boolean isEqual = (a == b);
        boolean isGreater = (a > b);
        System.out.println("Are they equal? " + isEqual);
        System.out.println("Is a greater than b? " + isGreater);
        
        // 3. Loops
        System.out.println("\n3. Loops:");
        
        // For loop
        System.out.println("For loop (0 to 4):");
        for(int i = 0; i < 5; i++) {
            System.out.println("  " + i);
        }
        
        // While loop
        System.out.println("While loop counting down from 5:");
        int count = 5;
        while(count > 0) {
            System.out.println("  " + count);
            count = count - 1;
        }
        
        // 4. Arrays
        System.out.println("\n4. Arrays:");
        
        // Creating an array
        int[] numbers = {1, 2, 3, 4, 5};
        System.out.println("Numbers array: " + java.util.Arrays.toString(numbers));
        
        // Accessing array elements
        System.out.println("First element: " + numbers[0]);
        System.out.println("Last element: " + numbers[4]);
        
        // Loop through array
        System.out.println("All elements:");
        for(int i = 0; i < numbers.length; i++) {
            System.out.println("  " + numbers[i]);
        }
        
        // 5. Static method example
        System.out.println("\n5. Static Method:");
        
        int result = addNumbers(10, 20);
        System.out.println("Result of adding 10 and 20: " + result);
        
        // 6. Strings
        System.out.println("\n6. Strings:");
        
        String text = "Hello, Java World!";
        System.out.println("Original text: " + text);
        
        // String operations
        String upperText = text.toUpperCase();
        String lowerText = text.toLowerCase();
        int textLength = text.length();
        
        System.out.println("Uppercase: " + upperText);
        System.out.println("Lowercase: " + lowerText);
        System.out.println("Length: " + textLength);
        
        // String concatenation
        String greeting = "Hello, ";
        String person = "Alice";
        String fullGreeting = greeting + person + "!";
        System.out.println("Greeting: " + fullGreeting);
        
        // 7. Inheritance example
        System.out.println("\n7. Inheritance:");
        
        // Create a dog object
        Dog myDog = new Dog("Buddy", "Golden Retriever");
        System.out.println(myDog.getInfo());
        System.out.println("Sound: " + myDog.makeSound());
        
        // Create a cat object
        Cat myCat = new Cat("Whiskers", "Orange");
        System.out.println(myCat.getInfo());
        System.out.println("Sound: " + myCat.makeSound());
        
        // 8. Access modifiers example
        System.out.println("\n8. Access Modifiers:");
        
        Person person1 = new Person("John", 25, "123-45-6789");
        System.out.println("Name: " + person1.getName());  // Public
        System.out.println("Age: " + person1.getAge());    // Protected (accessible)
        // System.out.println(person1.ssn);  // Private - not accessible directly
        
        // 9. Abstract class example
        System.out.println("\n9. Abstract Classes:");
        
        Shape rectangle = new Rectangle(5, 3);
        Shape circle = new Circle(4);
        
        System.out.println("Rectangle area: " + rectangle.calculateArea());
        System.out.println("Rectangle perimeter: " + rectangle.calculatePerimeter());
        System.out.println("Circle area: " + String.format("%.2f", circle.calculateArea()));
        System.out.println("Circle perimeter: " + String.format("%.2f", circle.calculatePerimeter()));
        
        // 10. Exception handling
        System.out.println("\n10. Exception Handling:");
        
        safeDivide(10, 2);
        safeDivide(10, 0);
        
        // 11. Collections
        System.out.println("\n11. Collections:");
        
        java.util.ArrayList<String> fruits = new java.util.ArrayList<>();
        fruits.add("apple");
        fruits.add("banana");
        fruits.add("orange");
        
        System.out.println("Fruits list: " + fruits);
        System.out.println("Number of fruits: " + fruits.size());
        
        // Add more fruits
        fruits.add("grape");
        System.out.println("After adding grape: " + fruits);
        
        // Check if contains
        boolean hasApple = fruits.contains("apple");
        System.out.println("Has apple? " + hasApple);
        
        // 12. Constructor example
        System.out.println("\n12. Constructors:");
        
        Student student1 = new Student("Alice", 20, "Computer Science");
        Student student2 = new Student("Bob", 19);
        
        System.out.println(student1.getStudentInfo());
        System.out.println(student2.getStudentInfo());
        
        System.out.println("\nJava assignment completed successfully!");
    }
    
    // Static method to add two numbers
    public static int addNumbers(int x, int y) {
        return x + y;
    }
    
    // Method to safely divide two numbers
    public static void safeDivide(int numerator, int denominator) {
        try {
            int result = numerator / denominator;
            System.out.println(numerator + " divided by " + denominator + " = " + result);
        } catch(ArithmeticException e) {
            System.out.println("Error: Cannot divide by zero!");
        }
    }
}

// Parent class for inheritance example
class Animal {
    protected String name;
    protected String species;
    
    public Animal(String name, String species) {
        this.name = name;
        this.species = species;
    }
    
    public String getInfo() {
        return name + " is a " + species;
    }
    
    public String makeSound() {
        return "Some sound";
    }
}

// Child class extending Animal
class Dog extends Animal {
    private String breed;
    
    public Dog(String name, String breed) {
        super(name, "Dog");  // Call parent constructor
        this.breed = breed;
    }
    
    public String getInfo() {
        return name + " is a " + breed + " " + species;
    }
    
    public String makeSound() {
        return "Woof!";
    }
}

// Another child class
class Cat extends Animal {
    private String color;
    
    public Cat(String name, String color) {
        super(name, "Cat");
        this.color = color;
    }
    
    public String getInfo() {
        return name + " is a " + color + " " + species;
    }
    
    public String makeSound() {
        return "Meow!";
    }
}

// Class to demonstrate access modifiers
class Person {
    public String name;        // Public - can be accessed from anywhere
    protected int age;         // Protected - accessible in same package and subclasses
    private String ssn;        // Private - only accessible within this class
    
    public Person(String name, int age, String ssn) {
        this.name = name;
        this.age = age;
        this.ssn = ssn;
    }
    
    // Public methods to access private data
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    public String getSSN() {
        return ssn;
    }
}

// Abstract class example
abstract class Shape {
    protected String name;
    
    public Shape(String name) {
        this.name = name;
    }
    
    // Abstract methods - must be implemented by subclasses
    public abstract double calculateArea();
    public abstract double calculatePerimeter();
}

// Rectangle class extending Shape
class Rectangle extends Shape {
    private double width;
    private double height;
    
    public Rectangle(double width, double height) {
        super("Rectangle");
        this.width = width;
        this.height = height;
    }
    
    public double calculateArea() {
        return width * height;
    }
    
    public double calculatePerimeter() {
        return 2 * (width + height);
    }
}

// Circle class extending Shape
class Circle extends Shape {
    private double radius;
    
    public Circle(double radius) {
        super("Circle");
        this.radius = radius;
    }
    
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
    
    public double calculatePerimeter() {
        return 2 * Math.PI * radius;
    }
}

// Student class with constructors
class Student {
    private String name;
    private int age;
    private String major;
    
    // Constructor with all parameters
    public Student(String name, int age, String major) {
        this.name = name;
        this.age = age;
        this.major = major;
    }
    
    // Constructor with just name and age (major defaults to "Undeclared")
    public Student(String name, int age) {
        this.name = name;
        this.age = age;
        this.major = "Undeclared";
    }
    
    public String getStudentInfo() {
        return name + ", age " + age + ", major: " + major;
    }
}