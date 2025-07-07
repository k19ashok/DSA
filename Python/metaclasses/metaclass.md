##### ➡️ Every class in python is an instace of `type` class

##### ➡️ Yes, `type` is a class and when an object is passed, it returns the type of the object

##### ➡️ When other args are passed, it returns a class instead 😮

- type(_name_, _bases_, _dct_):

- _name_ specifies the class name. This becomes the **name** attribute of the class.
- _bases_ specifies a tuple of the base classes from which the class inherits. This becomes the **bases** attribute of the class.
- _dct_ specifies a namespace dictionary containing definitions for the class body. This becomes the **dict** attribute of the class

```py
    >>> Foo = type('Foo', (), {})

    >>> x = Foo()
    >>> x
    <__main__.Foo object at 0x04CFAD50>
```

```py
    >>> Bar = type('Bar', (Foo,), dict(attr=100))

    >>> x = Bar()
    >>> x.attr
    100
    >>> x.__class__
    <class '__main__.Bar'>
    >>> x.__class__.__bases__
    (<class '__main__.Foo'>,)
```

##### ➡️ namespace is the dictionary of all the attributes and methods bound to the object. So, each object has a namespace to it

##### ➡️ There is a global namespace and module namespace I guess

##### ➡️ When we try to create an instance by calling `Foo()`, interpreter invokes the `__call__` method on the `Foo` object. If it doesn't have it defined, the parent's `__call__` method will be invoked. Every class's parent is `type` and hence `type` class's `__call__` method will be called.

##### ➡️ we can make use of `__new__` method to handle something before instantiating some class

##### We need to override the `__new__` of `type` class to define the behaviour or "customize the behaviour" before creating "a class"

```py
    >>> class Meta(type):
    ...     def __new__(cls, name, bases, dct):
    ...         x = super().__new__(cls, name, bases, dct)
    ...         x.attr = 100
    ...         return x
    ...
```

##### Define a new class Foo and specify that its metaclass is the custom metaclass Meta, rather than the standard metaclass type

```py
    >>> class Foo(metaclass=Meta):
    ...     pass
    ...
    >>> Foo.attr
    100
```


#### ➡️ So, basically a metaclass is a class for a class 😉
##### A class is a template for an object, and hence a metaclass is a template for a class

#### 💡 You use metaclasses when you need to perform actions or transformations at the time a class is defined


## Django's ORM

- Django's ORM is a classic and powerful example of metaclass usage. When you define a Django model,

    ```py
    from django.db import models

    class MyModel(models.Model):
        name = models.CharField(max_length=100)
        age = models.IntegerField()
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ['-created_at']
    ```

- How does Django know that name, age, and created_at should become database columns? 
- How does it automatically add methods like save(), delete(), objects.all()?

- The answer is a metaclass called `models.base.ModelBase`

- It uses these field definitions to build the database schema mapping.

- It dynamically adds methods like save(), delete(), and sets up the objects manager.

- It processes the Meta inner class to apply additional model options.

##### All this happens before `MyModel` even becomes a fully formed class object.
