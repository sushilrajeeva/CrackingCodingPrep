# Question 1: What are the main concepts in OOPS in Java?
# Solution:
    1. Inheritance
    2. Polymorphism
    3. Abstraction
    4. Encapsulation

    A. Inheritance
    Inheritance allows a class to inherit properties and methods from another class, promoting code reusability and establishing an 'is-a' relationship. The child class extends the parent class and can access its non-private members while adding its own specific functionality.
    
    Java supports single inheritance for classes but multiple inheritance for interfaces. The 'extends' keyword is used for class inheritance, and we can override parent methods to provide specific implementations

    Benefits include code reusability, method overriding for polymorphism, and establishing hierarchical relationships. I use inheritance when there's a clear 'is-a' relationship, like Car is-a Vehicle.

    B. Polymorhism (Overloading and Overriding)
    Polymorphism means 'many forms' - the same interface can have different implementations. In Java, we have runtime polymorphism through method overriding and compile-time polymorphism through method overloading. Runtime polymorphism allows the same method call to behave differently based on the actual object type

```Java
// Base class
abstract class Shape {
    abstract double calculateArea();
    abstract void draw();
}

// Different implementations
class Circle extends Shape {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    double calculateArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    void draw() {
        System.out.println("Drawing a Circle");
    }
}

class Rectangle extends Shape {
    private double length, width;
    
    public Rectangle(double length, double width) {
        this.length = length;
        this.width = width;
    }
    
    @Override
    double calculateArea() {
        return length * width;
    }
    
    @Override
    void draw() {
        System.out.println("Drawing a Rectangle");
    }
}

// Polymorphism in action
public class PolymorphismDemo {
    public static void main(String[] args) {
        // Same reference type, different object types
        Shape[] shapes = {
            new Circle(5),
            new Rectangle(4, 6),
            new Circle(3)
        };
        
        // Same method call, different behavior
        for (Shape shape : shapes) {
            shape.draw();           // Different implementation called
            System.out.println("Area: " + shape.calculateArea());
        }
    }
}
```
    This enables writing flexible code where the same interface works with different implementations. I use polymorphism extensively in service layers where different implementations can be swapped without changing client code.

    C. Abstraction
    Abstraction hides implementation details and shows only essential features to the user. It's achieved through abstract classes and interfaces. Abstract classes can have both concrete and abstract methods, while interfaces define pure contracts. This separates 'what' an object does from 'how' it does it.

    Abstraction reduces complexity by hiding unnecessary details. I use abstract classes when I need shared implementation, and interfaces when I need pure contracts. This makes code more maintainable and flexible.


    D. Encapsulation
    Encapsulation bundles data and methods together within a class and restricts direct access to internal data through access modifiers. It's achieved using private fields with public getter/setter methods, providing controlled access to object state and data validation.





# Question 2: What are Classes in Java?
# Solution:
    In Java, Classes are the collection of objects sharing similar characteristics and attributes. Classes represent the blueprint or template from which objects are created.  Classes are not real-world entities but help us to create objects which are real-world entities. 

# Questoin 3: What are Brief Access Specifiers and Types of Access Specifiers?
# Solution:
Access Specifiers in Java help to restrict the scope of a class, constructor, variable, method, or data member. There are four types of Access Specifiers in Java mentioned below:

    1. Public
    2. Private
    3. Protected
    4. Default

# Questoin 4: Where and how can you use a private constructor?
# Solution:
A private constructor is used if you don't want any other class to instantiate the object to avoid subclassing. The use private constructor can be seen as implemented in the example.

```Java
// Java program to demonstrate implementation of Singleton
// pattern using private constructors.
import java.io.*;
class GFG {
    static GFG instance = null;
    public int x = 10;
    // private constructor can't be accessed outside the
    // class
    private GFG() {}
    // Factory method to provide the users with instances
    static public GFG getInstance()
    {
        if (instance == null)
            instance = new GFG();
        return instance;
    }
}
// Driver Class
class Main {
    public static void main(String args[])
    {
        GFG a = GFG.getInstance();
        GFG b = GFG.getInstance();
        a.x = a.x + 10;
        System.out.println("Value of a.x = " + a.x);
        System.out.println("Value of b.x = " + b.x);
    }
}
```

# Questoin 5: What is an Interface?
# Solution:
An Interface in Java is a contract that defines what methods a class must implement, without providing the implementation itself. It's a reference type similar to a class but contains only abstract methods, default methods, static methods, and constants.
Key characteristics: All methods are implicitly public and abstract (before Java 8), all variables are implicitly public, static, and final constants. A class can implement multiple interfaces, solving Java's single inheritance limitation.

Interfaces enable multiple inheritance, loose coupling, and polymorphism. I use interfaces to define contracts between different layers - like Service interfaces for business logic, Repository interfaces for data access, and API contracts. They're essential for dependency injection where I depend on abstractions, not concrete implementations.

# Question 6: Difference between Abstract class and Interface?
# Solution:

I choose Abstract Class when I need shared code and state among related classes - like Vehicle with common properties but different implementations.

I choose Interface for capabilities that can be mixed into any class - like Serializable, Comparable, or custom behaviors.

Since Java 8, interfaces can have default methods, but the fundamental difference remains: Abstract classes are for inheritance hierarchies with shared implementation, while interfaces are for contracts and multiple capabilities.

# Question 7: Composition vs Aggregation vs Association?
# Solution:
These are three types of relationships between classes that represent different levels of dependency. Association is a general 'uses-a' relationship, Aggregation is 'has-a' with independent lifecycles, and Composition is 'part-of' with dependent lifecycles.

    1. Association - (Uses-A Relationship)
    Association represents a loose relationship where objects use each other but are independent. Neither object owns the other, and both can exist independently. It's the weakest form of relationship

```Java
// Association Example - Teacher and Student
class Student {
    private String name;
    private int studentId;
    
    public Student(String name, int studentId) {
        this.name = name;
        this.studentId = studentId;
    }
    
    public String getName() { return name; }
    public int getStudentId() { return studentId; }
}

class Teacher {
    private String name;
    private String subject;
    
    public Teacher(String name, String subject) {
        this.name = name;
        this.subject = subject;
    }
    
    // Association - Teacher teaches students but doesn't own them
    public void teach(List<Student> students) {
        System.out.println(name + " is teaching " + subject + " to " + students.size() + " students");
        for (Student student : students) {
            System.out.println("Teaching " + student.getName());
        }
    }
    
    public String getName() { return name; }
}

// Usage - Independent lifecycles
public class AssociationDemo {
    public static void main(String[] args) {
        // Students exist independently
        Student student1 = new Student("Alice", 101);
        Student student2 = new Student("Bob", 102);
        List<Student> students = Arrays.asList(student1, student2);
        
        // Teacher exists independently
        Teacher teacher = new Teacher("Dr. Smith", "Mathematics");
        
        // Association through method parameter
        teacher.teach(students);
        
        // Both can exist without each other
        // If teacher is deleted, students still exist
        // If students are deleted, teacher still exists
    }
}
```
Key characteristics: Loose coupling, both objects are independent, relationship is temporary or method-level. Like a teacher teaching students - they don't own each other.

    2. Aggregation - "Has-a" Relationship (Weak)
    Aggregation represents a 'has-a' relationship where one object contains others, but the contained objects can exist independently. It's a weak form of ownership - like a department having employees.

```Java
// Aggregation Example - Department and Employee
class Employee {
    private String name;
    private int employeeId;
    private double salary;
    
    public Employee(String name, int employeeId, double salary) {
        this.name = name;
        this.employeeId = employeeId;
        this.salary = salary;
    }
    
    public String getName() { return name; }
    public int getEmployeeId() { return employeeId; }
    public double getSalary() { return salary; }
    
    @Override
    public String toString() {
        return "Employee{" + name + ", ID: " + employeeId + "}";
    }
}

class Department {
    private String departmentName;
    private List<Employee> employees; // Aggregation - has employees
    
    public Department(String departmentName) {
        this.departmentName = departmentName;
        this.employees = new ArrayList<>();
    }
    
    // Add existing employees to department
    public void addEmployee(Employee employee) {
        if (employee != null && !employees.contains(employee)) {
            employees.add(employee);
            System.out.println(employee.getName() + " added to " + departmentName);
        }
    }
    
    public void removeEmployee(Employee employee) {
        if (employees.remove(employee)) {
            System.out.println(employee.getName() + " removed from " + departmentName);
        }
    }
    
    public void displayEmployees() {
        System.out.println("Employees in " + departmentName + ":");
        for (Employee emp : employees) {
            System.out.println("  " + emp);
        }
    }
    
    public List<Employee> getEmployees() {
        return new ArrayList<>(employees); // Return copy for safety
    }
}

// Usage - Independent lifecycles
public class AggregationDemo {
    public static void main(String[] args) {
        // Employees created independently
        Employee emp1 = new Employee("John Doe", 1001, 50000);
        Employee emp2 = new Employee("Jane Smith", 1002, 55000);
        Employee emp3 = new Employee("Mike Johnson", 1003, 48000);
        
        // Department created independently
        Department engineering = new Department("Engineering");
        Department marketing = new Department("Marketing");
        
        // Aggregation - department contains employees
        engineering.addEmployee(emp1);
        engineering.addEmployee(emp2);
        marketing.addEmployee(emp3);
        
        engineering.displayEmployees();
        
        // Employee can move between departments
        engineering.removeEmployee(emp2);
        marketing.addEmployee(emp2);
        
        // If department is deleted, employees still exist
        engineering = null; // Department deleted
        System.out.println("Employee still exists: " + emp1.getName());
    }
}
```

Key characteristics: 'Has-a' relationship, contained objects can exist independently, objects can belong to multiple containers. Like employees can work in different departments.


    3. Composition - "Part-of" Relationship (Strong)
    Composition represents a strong 'part-of' relationship where contained objects cannot exist without the container. When the parent is destroyed, children are also destroyed. It represents strong ownership.

```Java
// Composition Example - House and Room
class Room {
    private String roomType;
    private double area;
    
    public Room(String roomType, double area) {
        this.roomType = roomType;
        this.area = area;
        System.out.println(roomType + " created with area " + area + " sq ft");
    }
    
    public String getRoomType() { return roomType; }
    public double getArea() { return area; }
    
    @Override
    public String toString() {
        return roomType + " (" + area + " sq ft)";
    }
}

class House {
    private String address;
    private List<Room> rooms; // Composition - house owns rooms completely
    
    public House(String address) {
        this.address = address;
        this.rooms = new ArrayList<>();
        
        // House creates its own rooms - strong ownership
        createRooms();
        System.out.println("House created at " + address);
    }
    
    private void createRooms() {
        // Rooms are created by House and belong only to this House
        rooms.add(new Room("Living Room", 200.0));
        rooms.add(new Room("Kitchen", 120.0));
        rooms.add(new Room("Bedroom", 150.0));
        rooms.add(new Room("Bathroom", 80.0));
    }
    
    public void displayHouse() {
        System.out.println("House at " + address + " contains:");
        for (Room room : rooms) {
            System.out.println("  " + room);
        }
        System.out.println("Total rooms: " + rooms.size());
    }
    
    public double getTotalArea() {
        return rooms.stream().mapToDouble(Room::getArea).sum();
    }
    
    // When house is destroyed, rooms are also destroyed
    public void demolish() {
        System.out.println("Demolishing house at " + address);
        System.out.println("All rooms are destroyed with the house:");
        for (Room room : rooms) {
            System.out.println("  " + room.getRoomType() + " destroyed");
        }
        rooms.clear(); // Rooms cannot exist without house
    }
}

// Usage - Dependent lifecycles
public class CompositionDemo {
    public static void main(String[] args) {
        // House creates and owns its rooms
        House myHouse = new House("123 Main Street");
        myHouse.displayHouse();
        
        System.out.println("Total area: " + myHouse.getTotalArea() + " sq ft");
        
        // You cannot create rooms independently and add to house
        // Rooms are integral part of house structure
        
        // When house is destroyed, rooms are automatically destroyed
        myHouse.demolish();
        
        // Setting house to null destroys rooms too
        myHouse = null; // All rooms are gone with the house
    }
}
```

Key characteristics: Strong 'part-of' relationship, contained objects cannot exist independently, lifecycle dependency. Like rooms are part of a house - destroy house, rooms are gone too."

Examples
```Java
public class RealWorldExamples {
    
    // ASSOCIATION Examples:
    // - Doctor treats Patient
    // - Teacher teaches Student  
    // - Customer buys Product
    
    // AGGREGATION Examples:
    // - Department has Employees
    // - Team has Players
    // - Library has Books
    
    // COMPOSITION Examples:
    // - House has Rooms
    // - Car has Engine
    // - University has Departments (if departments can't exist independently)
}
```

# Question 8: Overloading vs Overriding
# Solution:
    Method overloading and overriding are both forms of polymorphism in Java, but they work differently and serve different purposes.
    
    Method Overloading is compile-time polymorphism where multiple methods have the same name but different parameters within the same class. The compiler decides which method to call based on the method signature.
    
    Method Overriding is runtime polymorphism where a child class provides a specific implementation of a method that's already defined in its parent class. The JVM decides which method to call based on the actual object type.

# Question 9: Can private method or static methods be overridden in Java?
# Solution:
    "No, neither private methods nor static methods can be overridden in Java, but for different reasons.
    
    Private Methods Cannot Be Overridden because they're not inherited by child classes. Private methods are only visible within the same class, so child classes cannot access or override them. If you create a method with the same name in a child class, it's a completely new method, not an override.
    
    Static Methods Cannot Be Overridden because they belong to the class, not to instances, and are resolved at compile-time based on the reference type. If you define a static method with the same signature in a child class, it's called 'method hiding', not overriding.

    Key Points:

    - Private methods: Not inherited, so cannot be overridden
    - Static methods: Belong to class, resolved at compile-time, method hiding occurs instead
    - Method hiding vs Overriding: Hiding is compile-time based on reference type, overriding is runtime based on object type
    - Only public, protected, and package-private instance methods can be truly overridden

    The fundamental rule is: overriding requires inheritance and runtime polymorphism, which private and static methods don't support."*
    Key message: Private = not inherited, Static = compile-time resolution, both cannot be overridden - only instance methods with proper visibility can be overridden.

# Question 10: Can main() Method Be Overloaded? 
# Solution:
    Yes, the main() method can be overloaded in Java, but only the standard signature public static void main(String[] args) will be called by the JVM as the entry point.
    
    You can create multiple main methods with different parameter types, but they're just regular overloaded methods that need to be called explicitly. The JVM specifically looks for the exact signature with String array parameter to start program execution

```
public class MainOverloadDemo {
    
    // ✅ Standard main - JVM entry point
    public static void main(String[] args) {
        System.out.println("Standard main method called by JVM");
        
        // Manually calling overloaded versions
        main(42);
        main(3.14);
        main();
    }
    
    // ✅ Overloaded main methods - valid but not entry points
    public static void main(int number) {
        System.out.println("Overloaded main with int: " + number);
    }
    
    public static void main(double number) {
        System.out.println("Overloaded main with double: " + number);
    }
    
    public static void main() {
        System.out.println("Overloaded main with no parameters");
    }
    
    // ❌ This won't be called by JVM - different return type
    public static int main(String[] args, int extra) {
        System.out.println("Another overloaded version");
        return extra;
    }
}
```

# Question 11: Can Abstract class have main method?
# Solution: 
Yes—an abstract class can have a main method. Since main is static, it doesn’t depend on instantiating the class. The JVM will happily invoke it as the entry point.

    -Why it works: static methods aren’t tied to an instance, so even though you can’t instantiate AbstractDemo, the JVM can still call AbstractDemo.main(...).

    - Key point: Only the exact signature public static void main(String[] args) is used by the JVM as the program entry.