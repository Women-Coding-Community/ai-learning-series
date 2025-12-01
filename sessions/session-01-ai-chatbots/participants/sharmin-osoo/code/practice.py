# Practice classes and functions 
# easy to reuse and group
''' method - a function that is assosicated with a class 
# example - an apploication for a company and we wanted to represent employees in our code 
# CASE STUDY -  we will need to create an employee class, so thta we don't have to reccreate this each time.
# the difference between a class and a class instance, A class is a blueprint for creating instances, and each unique employee we create 
# will be an an instance of that class. 
# instance variables - contain data that is unique to each instance'''

class Employee:
    #class variable 
    raise_amount = 1.04 
    num_of_employees = 0
     
    #initialise, or a constructor, when we create methods within a class they receive the instance as first argument
    def __init__ (self, first, last,pay):
        # we are now going to set all our methods in here, self is the instance, instance variables
        self.first =  first 
        self.last = last 
        self.pay = pay
        self.email = first + "." + last + "@company.com"
        #we are using the class variable because we wouldn't want the number of employees to be different for each instance
        Employee.num_of_employees += 1

# we create this method to display the full employee name, without having to write it out each time, we have to add the self  in the method  
    def fullname(self):
        return '{},{}'.format(self.first, self.last)
    def apply_raise(self):
        #this gives us the ability to change the raise_amount, using self will also allow override in subclass
        self.pay = int(self.pay * self.raise_amount)
    
#creating our instances of our employee class, we do not need to pass self as this is done automatically
empl_1 = Employee("Corey", "Chefer",50000)
empl_2 = Employee("Test", "Core",20000)
empl_3 = Employee("Sharmin", "Osoo", 35000)

# when we print this, it comes back as three as we instanciated employee three times , from line 33-35
print(Employee.num_of_employees)


# print(empl_1) # these are employee objects
# print(empl_2)

# print out the method, and we need to use the (parenthesis), if it was an attribute then it wouldn't need them
print(empl_1.fullname())

#email, pay, first and last name are all attributes of the class
print(empl_1.email)
print(empl_2.email)

# it is important to note that these two methods both do the same thing 
# this is the instance and then calling the method, self is passed automatically
empl_1.fullname()
#this is calling the method from the calss, we  have to pass in the instance. This shows what is happening above line 42
print(Employee.fullname(empl_1))


''' class variables should be the same for each instance
you can access the instance from the class variable '''
#print(Employee.raise_amount)
''' the instance below checks if it contains the attribute, or if any class or the class it inherits contains the attribute
in this case the instance is accessing the attribute through the class '''
# print(empl_1.raise_amount)
# print(empl_2.raise_amount)

#print(Employee.__dict__)
#   if we change the raise_amount variable in the class it will change it for all instances
Employee.raise_amount = 1.05
''' setting the raise amount in the instance, this will only change for employee 1 instance,because it created the attribute in emploee one
you can see this when you check this through empl_1.__dict__ '''
empl_1.raise_amount = 1.05

  






