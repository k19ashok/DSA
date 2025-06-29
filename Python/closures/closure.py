# Closure

# A function defined inside another function, and it's object is returned by the outer function
# This makes the inner function or the closure access the objects in it's non-local scope
# Simply, retaining the state even though it'll be outside of the enclosing scope

# Like the closure function carries a bag of hidden objects from it's enclosing function even after
# enclosing function's execution is completed

def outer_func(greeting):
    def inner_func(name):
        print(f"{greeting} {name}")
    return inner_func

hello_fun = outer_func("Hello")
hey_fun = outer_func("Hey")

hello_fun("Ashok")
hey_fun("Ashok")

# If you want to see what are all the values the closure function has access to
# closure_fun.__closure__ attribute is a tuple which contains the cells (objects)
# from it's enclosing scope

for cell in hello_fun.__closure__:
    print(cell.cell_contents)

for cell in hey_fun.__closure__:
    print(cell.cell_contents)

# During compile time, whenever an object is being referenced by the inner function
# Python treats those objects as "free variables" and creates cell objects for those in heap
# Whereas all local variables get memory allocated in the stack (remember stack frame)
# When these cells are freed? GC to the resue!

# BUT Assigning something to a variable with '=' is called binding, assigning to a mutable or immutable
# object needs nonlocal keyword
# ALSO..... If you're assiging something to a variable in the enclosing scope,
# compiler won't make the variable as a free variable! LEGB scoping rule

def outer_func():
    l = [1]

    print(id(l))
    def inner_func():
        l = [4, 5, 6, 7, 8, 9, 10, 11]
        print(id(l))
    # If you don't return l here, once the outer_func is executed, l will be popped from stack frame
    # and hence the same memory location could be used for the l in inner_func
    return inner_func, l

f, outer_l = outer_func()
print(outer_l)
f()
print(f.__closure__)



# USES

# factory functions

def root_calculator(n):
    def root(x):
        return x ** (1/n)
    return root

sqroot = root_calculator(2)
cbroot = root_calculator(3)

print(sqroot(4))
print(sqroot(5))
print(cbroot(27))


## STATEFUL FUNCS

def cumulative():
    l = []
    def average(val):
        l.append(val)
        return sum(l) / len(l)
    return average

avg = cumulative()

print(avg(1))
print(avg(2))
print(avg(3))
print(avg(4))
print(avg(5))


## CALLBACK FUNCTIONS
# When you want a function to have additional info and to be passed as arg to something else

def callback(text):
    def closure():
        print(f"Set label config to {text}")

    return closure

# button = tk.Button(
#     app,
#     text="Greet",
#     command=callback("Hello, World!"),
# )


## DECORATORS

# functions that take in another function as an argument and returns a new function with
# extended functionality from the passed function
# decorator function returns a closure
# @decorator can be used before a function definition, so that when the function is called,
# it's decorator will be called instead

# Memoization
# Logging
# Flask app.route
# Django login_required

# Encapsulation can be achieved with closures

def Stack():
    _items = []

    def push(x):
        _items.append(x)
    
    def pop():
        return _items.pop()
    
    def closure():
        pass

    closure.push = push
    closure.pop = pop
    return closure

s = Stack()
s.push(5)
print(s.pop())


# class with __call__ is a good choice in OO languages

class RootCalculator:
    def __init__(self, n):
        self.n = n
    
    def __call__(self, *args, **kwds):
        return args[0] ** (1 / self.n)

sqroot = RootCalculator(2)
cbroot = RootCalculator(3)

print(sqroot(4))
print(cbroot(8))