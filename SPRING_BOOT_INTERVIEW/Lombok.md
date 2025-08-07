# Java Interview Questions - Lombok, DI, Entity/DTO, Builder Pattern

# Question 1: What is Lombok and how does it help in Java development?
# Solution:
    Lombok is a Java library that reduces boilerplate code through compile-time annotation processing. Instead of writing repetitive getters, setters, constructors, and toString methods, I use annotations like @Data, @Builder, and @Slf4j to generate them automatically.
    
    For example, @Data combines @Getter, @Setter, @ToString, @EqualsAndHashCode, and @RequiredArgsConstructor into one annotation. This eliminates 80% of boilerplate code, reduces bugs in standard methods, and improves readability by focusing on business logic.
    
    The main benefits are fewer lines of code to maintain, consistent generated code, and improved developer productivity. However, there are trade-offs - the generated code isn't visible in source, requires IDE plugins, and can make debugging more complex.

# Question 2: Explain the difference between Entity and DTO. Why do we need both?
# Solution:
    Entity represents database tables with JPA annotations and handles relationships. DTO (Data Transfer Object) carries data between layers and external APIs.

    The key difference is purpose and exposure. Entity contains all database fields including sensitive data like passwords and internal notes, plus complex relationships. DTO provides controlled views - a UserResponseDto might only expose username and email, while hiding password and internal fields.

    We need both for security, API stability, and performance. Entity changes with database schema, but DTO provides stable API contracts. For example, I can change the database structure without breaking client applications because the DTO interface remains consistent. DTOs also prevent exposing sensitive data and reduce network payload by only transferring needed fields."

# Question 3: What is the Builder pattern and why use @Builder annotation?
# Solution:

    Builder pattern creates objects step-by-step with readable, flexible syntax. Instead of constructors with many parameters or setter chains, @Builder generates a fluent API.
    
    For example, instead of new User('john', 'email', 'password', true, 'ADMIN') where parameter order matters, I can write:

    ```Java
        User user = User.builder()
            .username('john')
            .email('email@test.com')
            .isActive(true)
            .role('ADMIN')
            .build();
    ```

    The benefits are readability - code reads like English, flexibility - can specify fields in any order and skip optional ones, and immutability - the built object can be immutable. @Builder is particularly useful for objects with many optional parameters or when creating test data with different combinations of fields.

# Question 4: What's the difference between field injection (@Autowired) and constructor injection?
# Solution:
    Field injection uses @Autowired on private fields where Spring uses reflection to set dependencies after object creation. Constructor injection passes dependencies through the constructor.

    Constructor injection is preferred because it makes dependencies explicit and visible in the constructor signature, enables easy unit testing without Spring context, catches circular dependencies at compile time, and ensures objects are fully initialized.

    Field injection creates mutable dependencies that can be changed after creation, makes testing difficult requiring reflection, and hides the complexity of a class's dependencies. It also risks NullPointerExceptions if injection fails.

    I use @RequiredArgsConstructor with final fields for clean constructor injection. This makes dependencies immutable, improves testability, and follows good design principles.


# Question 5: How do you handle dependency injection in Spring? What's @RequiredArgsConstructor?
# Solution:

    @RequiredArgsConstructor is a Lombok annotation that generates a constructor for all final fields and fields marked with @NonNull. Combined with Spring's constructor injection, it creates clean dependency injection.

    Instead of multiple @Autowired annotations, I declare dependencies as final fields and let Lombok generate the constructor. Spring automatically detects the constructor and injects dependencies.

    ```Java
        @Service
        @RequiredArgsConstructor
        public class UserService {
            private final UserRepository userRepository;
            private final EmailService emailService;
            // Lombok generates constructor, Spring injects dependencies
        }
    ```

    This approach is better than field injection because dependencies are immutable, explicit, and easily testable. The constructor clearly shows what the service needs, making the code self-documenting.

# Question 6: Can you walk through a complete CRUD operation showing Entity, DTO, and Builder usage?
# Solution:

    ```Java
        // Entity
        @Entity
        @Builder
        @Data // = @Getter + @Setter + @ToString + @EqualsAndHashCode + @RequiredArgsConstructor
        @NoArgsConstructor
        @AllArgsConstructor
        public class UserEntity {
            @Id @GeneratedValue
            private Long id;
            private String username;
            private String email;
            private String password;  // Sensitive - don't expose
        }

        // Request DTO
        @Builder
        @Data
        public class CreateUserRequest {
            @NotBlank
            private String username;
            @Email
            private String email;
            private String password;
        }

        // Response DTO
        @Builder
        @Data
        public class UserResponse {
            private Long id;
            private String username;
            private String email;
            // No password - security
        }

        // Service
        @Service
        @RequiredArgsConstructor
        public class UserService {
            private final UserRepository repository;
            
            public UserResponse createUser(CreateUserRequest request) {
                UserEntity entity = UserEntity.builder()
                    .username(request.getUsername())
                    .email(request.getEmail())
                    .password(encode(request.getPassword()))
                    .build();
                    
                UserEntity saved = repository.save(entity);
                
                return UserResponse.builder()
                    .id(saved.getId())
                    .username(saved.getUsername())
                    .email(saved.getEmail())
                    .build();
            }
        }
    ```
    
# Question 7: What are some Lombok annotations you commonly use and their purposes?
# Solution:
    I commonly use several Lombok annotations:
    
    - @Data - Combines @Getter, @Setter, @ToString, @EqualsAndHashCode, and @RequiredArgsConstructor. Perfect for simple data classes.
    - @Builder - Generates builder pattern implementation. Great for objects with many optional fields.
    - @RequiredArgsConstructor - Generates constructor for final fields. Essential for dependency injection.
    - @Slf4j - Automatically creates a logger field. Eliminates boilerplate logging setup.
    - @Value - Creates immutable classes with only getters. Useful for value objects.
    - @NoArgsConstructor/@AllArgsConstructor - Generates constructors. Often needed for JPA entities.
    
    For example, @Data @Builder @NoArgsConstructor @AllArgsConstructor covers most needs for JPA entities, while @Builder @Value works well for immutable DTOs.

# Question 8: What are some Lombok annotations you commonly use and their purposes?
# Solution:
    I use Bean Validation annotations on DTO fields and @Valid in controller methods:

    ```Java
        @Builder
        @Data
        public class CreateUserRequest {
            @NotBlank(message = 'Username is required')
            @Size(min = 3, max = 50)
            private String username;
            
            @Email(message = 'Invalid email format')
            @NotBlank
            private String email;
            
            @Size(min = 8, message = 'Password must be at least 8 characters')
            private String password;
        }

        @PostMapping('/users')
        public ResponseEntity<UserResponse> createUser(@Valid @RequestBody CreateUserRequest request) {
            // Spring automatically validates and returns 400 if invalid
            return ResponseEntity.ok(userService.createUser(request));
        }
    ```

    This approach separates validation rules from business logic, provides clear error messages, and works automatically with Spring's validation framework. Different DTOs can have different validation rules for the same entity fields.

# Question 9: What are the disadvantages of using Lombok?
# Solution:
    Lombok has several disadvantages to consider:

        - Hidden complexity - generated code isn't visible in source, making debugging harder. IDE dependency - requires plugins for proper support, and team members need to install them.

        - Version compatibility - Lombok updates can break builds, and it sometimes conflicts with newer Java versions. Debugging difficulty - stepping through generated code can be challenging.

        - Annotation overuse - easy to misuse or over-apply annotations. Learning curve - team members need to understand what each annotation generates.
    
        - Magic behavior - @Data might generate equals/hashCode that don't behave as expected for certain field types.
        - Despite these drawbacks, I find the productivity benefits usually outweigh the costs for most projects, but I'm careful not to overuse it and ensure the entire team understands the implications.

# Question 10: How would you refactor legacy code from field injection to constructor injection?
# Solution:
    I follow a systematic approach:

    - First, identify all @Autowired fields and convert them to final fields. Add @RequiredArgsConstructor to the class or manually create the constructor.

    ```Java
        // Before
        @Service
        public class LegacyService {
            @Autowired private RepoA repoA;
            @Autowired private RepoB repoB;
        }

        // After
        @Service
        @RequiredArgsConstructor
        public class ModernService {
            private final RepoA repoA;
            private final RepoB repoB;
        }
    ```

    - Then update unit tests to use constructor instead of reflection. Remove any @Autowired annotations and Spring test dependencies for unit tests.

    - I do this incrementally, class by class, and run tests after each change. The refactoring immediately reveals if a class has too many dependencies. If the constructor becomes unwieldy, it indicates the class might violate Single Responsibility Principle and need to be split

