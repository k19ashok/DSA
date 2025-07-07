# Global Interpreter Lock

##### Only one thread can have the control of python interpreter at a particular point in time

##### Which means only one thread can be in a state of execution

##### objects created in Python have a reference count variable that keeps track of the number of references that point to the object

```py
    >>> import sys
    >>> a = []
    >>> b = a
    >>> sys.getrefcount(a)
    3
```

#### The problem was that this reference count variable needed protection from **race conditions** where two threads increase or decrease its value simultaneously

#### This would have caused memory leaks, or improper release of memory even if there are references

#### We can have a lock for each object in python - this can cause "deadlocks" and decreased performace

### So, how about a lock on the interpreter itself? no deadlocks, not really bad performance, but single-threaded :(

##### Other languages use garbage collection instead of reference counting for thread safe memory management

#### Python has been around since the days when operating systems did not have a concept of threads

## CPU Bound vs I/O Bound

#### CPU-bound programs are those that are pushing the CPU to its limit. This includes programs that do mathematical computations like matrix multiplications, searching, image processing, etc.

#### I/O-bound programs are the ones that spend time waiting for Input/Output which can come from a user, file, database, network, etc. I/O-bound programs sometimes have to wait for a significant amount of time till they get what they need from the source due to the fact that the source may need to do its own processing before the input/output is ready.

### Multi threading in python for CPU bound tasks increase the execution time when compared to single threaded execution
