# Spring Boot Interview Questions - Core Concepts

# Question 1: What is @SpringBootApplication annotation and what does it do internally?
# Solution:
    "@SpringBootApplication is a meta-annotation that combines three essential annotations:

```Java
    @SpringBootApplication
    // Equivalent to:
    // @SpringBootConfiguration  
    // @EnableAutoConfiguration
    // @ComponentScan
    public class MyApplication {
        public static void main(String[] args) {
            SpringApplication.run(MyApplication.class, args);
        }
    }
```

@SpringBootConfiguration enables Java-based configuration, @EnableAutoConfiguration automatically configures beans based on classpath dependencies, and @ComponentScan scans for components in the current package and sub-packages.

When the application starts, Spring Boot creates an ApplicationContext, registers auto-configured beans, scans for components with annotations like @Service, @Repository, @Controller, and wires dependencies together. This eliminates the need for extensive XML configuration and provides sensible defaults out of the box.

# Question 2: Explain IoC (Inversion of Control) Container and how Spring implements it.
# Solution:
    IoC Container inverts the control of object creation and dependency management from the application code to the framework. Instead of objects creating their dependencies, the container provides them.

    In laymen term instead of us creating and maintaing objects, the Spring Boot will take care of creating these objects as beans,
    and stores these beans in IoC container. We then use Application Context (that implements the IoC) container to fetch beans from.
    The files marked with @Component or its subsideary will be automatically configured to beans and will be used to serve these beans
    to any file that @autowires these as their instance variable

```Java
    // Without IoC - tight coupling
    public class UserService {
        private UserRepository repository = new UserRepository(); // Hard dependency
        
        public void createUser(User user) {
            repository.save(user);
        }
    }

    // With IoC - loose coupling
    @Service
    public class UserService {
        private final UserRepository repository;
        
        public UserService(UserRepository repository) { // Dependency injected
            this.repository = repository;
        }
        
        public void createUser(User user) {
            repository.save(user);
        }
    }
```

Spring's IoC container (ApplicationContext) manages the complete lifecycle - it creates objects, configures them, assembles dependencies, and manages their destruction. This provides loose coupling, easier testing with mock objects, and centralized configuration management. The container acts as a factory that knows how to create and wire objects based on configuration metadata.

In Spring Boot, ApplicationContext is automatically created and configured. It loads all auto-configurations, scans components, and makes beans available for injection throughout the application lifecycle.

# Question 3: How does Component Scanning work in Spring Boot?
# Solution:
    Component scanning automatically discovers and registers beans by scanning classpath for classes annotated with stereotype annotations.

```Java
    @SpringBootApplication
    public class Application {
        // By default scans current package and sub-packages
    }

    // These will be automatically discovered:
    @Controller
    @RequestMapping('/users')
    public class UserController { }

    @Service  
    public class UserService { }

    @Repository
    public class UserRepository { }

    @Component
    public class EmailUtil { }

    // Custom component scan
    @SpringBootApplication
    @ComponentScan(basePackages = {'com.myapp.service', 'com.myapp.repository'})
    public class Application { }

    // Exclude specific classes
    @SpringBootApplication
    @ComponentScan(excludeFilters = @Filter(type = FilterType.ASSIGNABLE_TYPE, 
                                        classes = TestConfiguration.class))
    public class Application { }
```

Spring Boot scans from the main application class package downwards. It looks for @Component, @Service, @Repository, @Controller annotations and creates beans automatically. The scanning happens during application startup, and discovered beans are registered in the ApplicationContext for dependency injection.

# Question 4: How does Component Scanning work in Spring Boot?
# Solution:
    Spring supports three types of dependency injection:

```Java
    // 1. Constructor Injection (Recommended) (Can be simplified with lombok)
    @Service
    public class UserService {
        private final UserRepository repository;
        private final EmailService emailService;
        
        public UserService(UserRepository repository, EmailService emailService) {
            this.repository = repository;
            this.emailService = emailService;
        }
    }

    // 2. Setter Injection
    @Service
    public class UserService {
        private UserRepository repository;
        
        @Autowired
        public void setRepository(UserRepository repository) {
            this.repository = repository;
        }
    }

    // 3. Field Injection (Not recommended)
    @Service
    public class UserService {
        @Autowired
        private UserRepository repository;
    }
```

Constructor injection is recommended because it ensures immutable dependencies, makes dependencies explicit, enables easy unit testing without Spring context, catches circular dependencies at compile time, and guarantees objects are fully initialized.
Field injection should be avoided as it creates mutable dependencies, requires reflection for testing, and hides complexity. Setter injection is useful for optional dependencies but makes objects mutable after construction

# Question 5: What happens during Spring Boot application startup? Walk me through the process.
# Solution:
    Spring Boot application startup follows these key phases:

```Java
@SpringBootApplication
// Equivalent to:
// @SpringBootConfiguration  
// @EnableAutoConfiguration
// @ComponentScan
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

    1. SpringApplication Creation: Creates SpringApplication instance and configures sources
    2. Environment Preparation: Loads application.properties/yml, system properties, environment variables
    3. ApplicationContext Creation: Creates appropriate context type (web/non-web)
    4. Auto-Configuration: @EnableAutoConfiguration kicks in, analyzes classpath and configures beans automatically
    5. Component Scanning: @ComponentScan discovers and registers beans from specified packages
    6. Bean Instantiation: Creates singleton beans, resolves dependencies, performs dependency injection
    7. Post-Processing: Applies BeanPostProcessors, initializes beans
    8. Application Ready: Fires ApplicationReadyEvent, application is ready to serve requests

    Each phase can be customized through ApplicationListeners, BeanPostProcessors, or custom auto-configurations. The entire process is driven by conventions and auto-configuration to minimize manual setup.

