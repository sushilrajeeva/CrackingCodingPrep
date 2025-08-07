# Question 1. What key features were added in Java 8?
# Solution:
    1. Lambda Expressions
    2. Stream API
    3. Functional Interfaces
    4. Optional Class
    5. java.time Date/Time – immutable, timezone-aware classes like LocalDateTime, replacing the old java.util.Date pain points.

# Question 2. What is Functional Interface (also called SAM -> Single Abstract Method)?
# Solution:
    If we define an interface with only one abstract method then that interface is called Functional Interface.
    When we declare an interface as @FunctionalInterface then that interface can only have one abstract method,
    if we try to add more abstract method, it will throw compiler error.
    Note: only one abstract method is allowed but we can have default, static or object class methods

# Question 3. What is Lambda Expressions?
# Solution:
    Lambda expressions enable functional programming in Java by allowing you to write anonymous functions concisely.

    ```Java
        // Before Java 8
        List<String> names = Arrays.asList("Bob", "Alice", "Charlie");

        // Before Java 8 - lots of code for simple sorting
        Collections.sort(names, new Comparator<String>() {
            @Override
            public int compare(String s1, String s2) {
                return s1.compareTo(s2);
            }
        });

        // Java 8 - clean and simple
        Collections.sort(names, (s1, s2) -> s1.compareTo(s2));

        // Even simpler
        Collections.sort(names, String::compareTo);
    ```

# Question 4. What is Optional Class?
# Solution:
    Optional<T> is a container class that uses generics. It's designed to represent a value that might or might not be present, helping avoid NullPointerException. Same as Python's Optional

    Optional is Java 8's solution to the 'billion-dollar mistake' - null references. Instead of returning null and hoping callers remember to check, I return Optional to make it explicit that a value might not exist.
    
    The main benefit is it eliminates NullPointerExceptions through compile-time safety. I can chain operations like map and filter without worrying about null checks. For example, instead of nested if-statements checking user, then address, then city, I can write user.map(getAddress).map(getCity).orElse('Unknown').
    
    I use it primarily for return types in methods that might not find data - like repository lookups or config retrievals. It makes the API contract clear and forces callers to handle the 'not found' case explicitly. The code becomes more self-documenting and safer.

    ```Java
        // Optional is generic - the <T> indicates it can hold any type
        Optional<String> optionalString = Optional.of("Hello");
        Optional<Integer> optionalInt = Optional.of(42);
        Optional<User> optionalUser = Optional.empty();

        // Usage:
        public Optional<String> getConfigValue(String key) {
            return Optional.ofNullable(properties.getProperty(key));
        }

        // Usage
        String timeout = getConfigValue("timeout")
            .orElse("30");
    ```

# Question 5. How do lambda expressions differ from anonymous classes?
# Solution:
    Anonymous classes create an extra .class file, carry their own scope, and their this points to the anonymous object. Lambdas are compiled to invokedynamic calls that reference a functional interface instance—so they’re lighter. They inherit this from the enclosing class, can capture effectively-final variables, and give you much shorter syntax. Performance-wise they avoid the anonymous-class allocation in most cases.

    Note : Key Takeaway: Lambda = quick and light, Anonymous class = powerful but heavy

# Question 6: Explain the Streams API and when you’d use parallel streams.
# Solution:
    Streams API lets me process collections functionally instead of imperatively. Instead of writing loops with if-statements and manual list building, I chain operations like filter, map, and collect. It's more readable and less error-prone.
    
    For parallel streams, I use them when I have large datasets with CPU-intensive operations. For example, processing thousands of records where each record needs complex validation or transformation. The rule of thumb is: if dataset size times operation cost is greater than parallelization overhead, go parallel.


# Question 7: Interface vs. abstract class—when do you choose which?.
# Solution:
    Interface: pure contract—multiple inheritance allowed. Since Java 8, you can add default and static methods for common behavior but you still can’t hold state.
    
    Abstract class: single inheritance, but you can define fields, constructors, and both abstract and concrete methods.

    When I choose:
    • If I only need to promise capabilities—Comparable, Serializable—I use an interface.
    • When I want to share common state or protected utility methods—say, a BaseRepository that caches a DataSource—I go abstract class.
    In practice I start with interfaces plus default methods; I switch to an abstract base only when shared state is unavoidable.

    Simple answer:
        The main difference is abstract classes support single inheritance with shared state and behavior, while interfaces support multiple inheritance for defining contracts.

        I choose abstract classes when I have an 'is-a' relationship and need shared code - like Vehicle with common properties like brand, model, and shared methods like startEngine(), but each vehicle type accelerates differently.

        I choose interfaces for 'can-do' relationships and multiple capabilities - like Drawable, Serializable, Cacheable. A class might be drawable AND serializable, so interfaces give that flexibility.

        Since Java 8, interfaces can have default methods, blurring the lines, but the key distinction remains: abstract classes are for shared inheritance hierarchies, interfaces are for contracts and multiple capabilities.

        In practice, I often use both - an abstract base class for core functionality, plus interfaces for optional features that can be mixed and matched.

# Question 8: HashMap vs. ConcurrentHashMap—what’s the difference?
# Solution:
    HashMap is fast but not thread-safe - using it with multiple threads can cause data corruption, infinite loops, or unexpected behavior. ConcurrentHashMap is designed for multi-threaded environments with internal thread-safety mechanisms.

    The key differences: HashMap allows null keys/values and is faster, while ConcurrentHashMap doesn't allow nulls but handles concurrent access safely. HashMap uses fail-fast iterators that throw exceptions if modified during iteration, while ConcurrentHashMap uses weakly consistent iterators.

    I use HashMap for single-threaded scenarios like local caches or temporary data structures where performance is critical. I use ConcurrentHashMap in web applications, shared caches, or any multi-threaded environment where multiple threads need to access the same map.

    ConcurrentHashMap also provides atomic operations like computeIfAbsent() and merge() that are invaluable for thread-safe updates without external synchronization.

# Question 9: How does the Java Memory Model guarantee visibility with the volatile keyword?
# Solution:
    The Java Memory Model allows threads to cache variables locally for performance. Without proper synchronization, Thread A might update a variable but Thread B never sees the change because it's reading from its local cache.

    Volatile solves this by creating memory barriers. When I write to a volatile variable, it creates a store-store barrier that flushes all previous writes to main memory. When I read a volatile variable, it creates a load-load barrier that forces reading from main memory and invalidates local caches.
    
    The key guarantee is the happens-before relationship: everything that happened before a volatile write is visible to threads that perform a volatile read of that same variable. This creates a synchronization point where threads can safely exchange data.
    
    The performance cost comes from memory barriers preventing CPU optimizations and forcing main memory access instead of fast cache access. It's much lighter than synchronized blocks but heavier than regular variables - typically 2-10x slower depending on the CPU architecture.

# Question 9: What is Atomic in java and how does it ensure thread safety?
# Solution:

    Atomic classes in Java like AtomicInteger, AtomicLong, and AtomicBoolean provide lock-free thread safety using Compare-And-Swap (CAS) operations. Unlike synchronized blocks that use locks, atomic operations use hardware-level CAS instructions that atomically check and update values in a single CPU instruction.
    
    The key mechanism is CAS - it compares the current value with an expected value, and only updates if they match. If another thread changed the value, CAS fails and retries. This ensures that operations like increment, add, or compare-and-set happen atomically without blocking other threads.
    
    This makes atomic classes faster than synchronized blocks for simple operations like counters or flags, and eliminates the risk of deadlocks since no locks are involved.

    Counter question - what happen when two threads are read and updated same time how CAS ensure thread safety?
    SOl : When two threads read the same value and try to CAS at the same time, the hardware guarantees only one CAS succeeds. The failed thread immediately retries with the new current value. This happens in a tight loop until success.
    
    For example, if Thread A and B both read counter=5 and try to increment, one CAS(5,6) succeeds and the other fails. The failed thread re-reads counter=6, calculates next=7, and tries CAS(6,7), which succeeds.
    
    This lock-free approach is faster than synchronized blocks because threads don't wait - they immediately retry. The hardware CAS instruction ensures atomicity, and the retry loop ensures progress without data loss

    ```Java
        import java.util.concurrent.atomic.AtomicInteger;

        public class AtomicSolution {
        private AtomicInteger counter = new AtomicInteger(0);  // Atomic operations!

        public void increment() {
            counter.incrementAndGet();  // Single atomic operation - no interference possible
        }

        public int getValue() {
            return counter.get();       // Always gets current value
        }

        // Other atomic operations
        public void example() {
            counter.addAndGet(5);           // Add 5 atomically
            counter.compareAndSet(10, 20);  // If value is 10, set to 20
            int old = counter.getAndSet(0); // Get current, then set to 0
        }
        }
    ```


# Question 9: What is Synchronized in java and how does it ensure thread safety?
# Solution:
    Synchronized provides thread safety through mutual exclusion locks. When a thread enters a synchronized method or block, it acquires a lock on the specified object, and no other thread can enter any synchronized section using that same lock until it's released.
    
    Think of it like a single-person bathroom - only one person can use it at a time. Other threads must wait outside until the current thread finishes and 'unlocks the door.'
    
    I use synchronized when I need to protect multiple operations that must happen together atomically - like transferring money between accounts where I need to check balance, deduct from source, and add to destination as one unit.
    
    The trade-off is performance - synchronized blocks threads, which can cause bottlenecks if one thread is slow. For simple operations like counters, I prefer AtomicInteger because it's non-blocking and faster. For complex multi-step operations, synchronized is the right choice despite the performance cost.
    
    Key pitfall is deadlock risk when using multiple locks - always acquire locks in consistent order to avoid it.

    ```Java
        public class SynchronizedTypes {
            private int instanceVar = 0;
            private static int staticVar = 0;
            
            // 1. Synchronized method - uses 'this' as lock
            public synchronized void method1() {
                instanceVar++; // Lock: this object
            }
            
            // 2. Synchronized static method - uses Class object as lock
            public static synchronized void staticMethod() {
                staticVar++; // Lock: SynchronizedTypes.class
            }
            
            // 3. Synchronized block - custom lock object
            public void method3() {
                synchronized(this) {
                    instanceVar++; // Same as synchronized method
                }
            }
            
            // 4. Synchronized with custom object
            private final Object customLock = new Object();
            public void method4() {
                synchronized(customLock) {
                    instanceVar++; // Lock: customLock object
                }
            }
        }
    ```

# Quick Folloups
## a. "When do you use volatile?"
## b. "For simple flags and status variables that need immediate visibility across threads, but don't need atomic updates."
## c. "When do you use Atomic classes?"
## d. "For counters, IDs, or any numeric operations that multiple threads need to modify safely without synchronization blocks."
## e. "Performance difference?"
## f. "Volatile < Atomic < Synchronized (from fastest to slowest), but atomic is much faster than synchronized for simple operations."
## g. This gives you clear, simple explanations that show you understand the practical differences and when to use each approach!

# Question 10: Ways to achieve synchronization in Java.
# Solution:
    Java provides multiple synchronization mechanisms depending on the use case. For simple operations like counters or flags, I use Atomic classes or volatile - they're non-blocking and high-performance. For complex multi-step operations, synchronized keyword or ReentrantLock work well, though they're blocking.

    The java.util.concurrent package offers advanced options: ConcurrentHashMap for thread-safe collections, ReadWriteLock for read-heavy scenarios, and high-level synchronizers like CountDownLatch for coordination.

    I choose based on complexity and performance needs: Atomic for simple operations, synchronized for complex logic, concurrent collections for shared data structures, and synchronizers for thread coordination. The key is understanding the trade-offs between blocking vs non-blocking, performance vs simplicity, and choosing the right tool for the specific synchronization requirement.

# Question 11: What is Reentrant Lock.
# Solution:

    ReentrantLock is Java's explicit lock implementation that provides more features than synchronized. 'Reentrant' means the same thread can acquire the lock multiple times without deadlocking - useful when one synchronized method calls another.
    
    The key advantages over synchronized are timeout capability with tryLock(), interruptible locking with lockInterruptibly(), and fairness options to prevent thread starvation. You can also get lock information like hold count and queue length for monitoring.

    The trade-off is complexity - you must manually lock and unlock in try-finally blocks, while synchronized handles this automatically. I use ReentrantLock when I need the advanced features like timeouts or fairness, and synchronized for simple mutual exclusion where the automatic lock management is preferred.

    Common pitfall is forgetting to unlock or not using try-finally, which can cause deadlocks. Always unlock in finally block to ensure proper cleanup even when exceptions occur