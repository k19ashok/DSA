# Functions are first class objects in python
# Inner functions are not defined until the parent function is called
# which means the inner functions are locally scoped to the outer function

# A decorator wraps a function, modifying its behavior.
# @decorator

def do_twice(func):
    def wrapper(*args, **kwargs):
        for _ in range(2):
            func(*args, **kwargs)
        return "Done"
    return wrapper

@do_twice
def say_hello():
    print("Hello")

status = say_hello()
print(status)


# Introspection is the ability of an object to know about its own attributes at runtime.
# For instance, a function knows its own name and documentation

# @functools.wraps for retaining the called function attributes
# Meaning that the wrapped function should not interfere with the actual function's introspection

# The @functools.wraps decorator uses functools.update_wrapper() to update special attributes 
# like __name__ and __doc__ that are used in the introspection

import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper

# Applications
# @timer
# @debug - to print the args and return value of a function
# @slow_down - sleep for sometime before executing the function, in cases of polling an API
# @login_required

# @classmethod
# @staticmethod
# @property


# Decorators can get args by making the decorator itself a closure to another function
# Decorators don’t have to wrap the function that they’re decorating
# They can also simply register that a function exists and return it unwrapped

PLUGINS = dict()

def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func


# We can accept decorators with or without args, based on that we've to return either decorator or the inner function

def repeat(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)


# Assigning values as function attributes make sense for stateful decorators

def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__}()")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0  # here we are assigning num_calls as an attribute to func
    # this makes it easily accessible outside when compared to closures
    return wrapper_count_calls


## CLASS DECORATORS

# class decorators are similar to function decorators where __init__ will take the func as arg
# and __call__ is responsible for behaving like a wrapper function and return self

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__}()")
        return self.func(*args, **kwargs)


# @dataclass

# None, True, False are singletons
def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if wrapper_singleton.instance is None:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton

## Input validation in Flask route

from flask import abort, request
def validate_json(*expected_args):
    def decorator_validate_json(func):
        @functools.wraps(func)
        def wrapper_validate_json(*args, **kwargs):
            json_object = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_object:
                    abort(400)
            return func(*args, **kwargs)
        return wrapper_validate_json
    return decorator_validate_json

# @app.route("/grade", methods=["POST"])
@validate_json("student_id")  # we can pass the keys that we want from any function DRY
def update_grade():
    json_data = request.get_json()
    return "success!"

