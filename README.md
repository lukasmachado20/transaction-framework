# Learning Decorators 

### How decorators work and for what purpose

- Decorators is a form to involve a method with another method adding a specfic funcionality without change the decorated method.
- Decorators they are used when the code needs a specifc function that's used in other parts of code and don't make part o logic of code. 

* Decorators receive functions as parameters and return another function
* Generally decorators is a callable that's returns another callable


### Advantages:
* Avoid code duplication
* Separate Responsability 
* Used for Cross-cutting concerns 

### What is Cross-cutting concerns?
- Cross-cutting concerns are funcionalities of a software that is used in diferents parts of the system but is not part of the main logic of the program.
- Examples are: Logs, Cache, Authentication, Permissions, Database transactions, Error Treatment...
