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