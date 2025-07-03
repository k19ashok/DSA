import os


# Use try - finally to manage resource

wrong = "\u0336" + "\u0336".join("wrong")

f = open("C:\\Users\\k19as\\Desktop\Programming\DSA\Python\closures\closure.py", "w")
try:
    f.write("")
    raise ValueError("Chummaa 😘")
except ValueError:
    print(f"Something {wrong}, nope cute happened!")
finally:
    f.close()
    print("File Closed!")


## with statement creates a runtime context that allows you to run a group of statements under the control of a context manager
## context management protocol consists of two special methods
## .__enter__() is called by the with statement to enter the runtime context
## .__exit__() is called when the execution leaves the with code block

## with keyword only works with objects that support context management protocol

## Multiple context managers are supported


class A:
    def __enter__(self):
        print("A enter")

    def __exit__(self, _, __, ___):
        print("A exit")


class B:
    def __enter__(self):
        print("B enter")

    def __exit__(self, _, __, ____):
        print("B exit")


with A() as a, B() as b:
    pass


# os.scandir()
a = 5
with os.scandir(".") as entries:
    for entry in entries:
        print(entry.name, "->", entry.stat().st_size, "bytes")


# Decimal localcontext precision

from decimal import Decimal, localcontext

with localcontext() as ctx:
    ctx.prec = 42  # defaults to 28
    print(Decimal("1") / Decimal("42"))

# Decimal('0.0238095238095238095238095238095238095238095')


## threading.Lock()

import threading

balance_lock = threading.Lock()

# try finally
balance_lock.acquire()
try:
    pass
finally:
    balance_lock.release()

# with
with balance_lock:
    pass

print(balance_lock.__enter__)


## asyncio, aiohttp
## asynchronous context manager

import aiohttp


async def check(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"{url}: status -> {response.status}")
            html = await response.text()
            print(f"{url}: type -> {html[:17].strip()}")


## Asynchronous context managers implement the special methods .__aenter__() and .__aexit__()
## The async with ctx_mgr construct implicitly uses await ctx_mgr.__aenter__() when entering
## the context and await ctx_mgr.__aexit__() when exiting it


## You can also create custom function-based context managers using the contextlib.contextmanager decorator
## with context managers, you can perform any pair of operations that needs to be done
## before and after another operation or procedure

## If the .__exit__() method returns True, then any exception that occurs in the with block is swallowed
# and the execution continues at the next statement after with. If .__exit__() returns False
# then exceptions are propagated. This is also the default behavior when the method doesn’t return anything explicitly.

## return value of __enter__ is assigned to the variable specified with as

## A common trick when you don’t remember the exact signature of .__exit__() and don’t need to access its arguments
# is to use *args and **kwargs like in def __exit__(self, *args, **kwargs)

# SOME EXAMPLE


class WritableFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        f = open(self.file_path, "w")
        self.f = f
        return f

    def __exit__(self, _, __, ___):
        if self.f:
            self.f.close()


with WritableFile("./sample.txt") as f:
    f.write("HELLO!")


## Context manager as a timer

# timing.py

from time import perf_counter, sleep


class Timer:
    def __enter__(self):
        self.start = perf_counter()
        self.end = 0.0
        return lambda: self.end - self.start

    def __exit__(self, *args):
        self.end = perf_counter()


with Timer() as timer:
    sleep(1)
print(timer())

## @contextmanager decorator

from contextlib import contextmanager


@contextmanager
def writable_file(file_path):
    file = open(file_path, mode="w")
    try:
        yield file
    finally:
        file.close()


with writable_file("hello.txt") as file:
    file.write("Hello, World!")

##

from contextlib import contextmanager
from time import time


@contextmanager
def mock_time():
    global time
    saved_time = time
    time = lambda: 42
    yield
    time = saved_time


with mock_time():
    print(f"Mocked time: {time()}")

# Mocked time: 42

time()
# 1616075222.4410584


# a common practice when you’re writing asynchronous context managers is to implement
# both sync and async special methods for enter and exit
