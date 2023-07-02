Thread-safe and process-safe singleton class.
The singleton is shared between all threads.
For every process, a new instance is initialized and shared between all threads of the process.

Use like this:
```
from pyngleton import Singleton

class MyClass(Singleton):
    pass

a = MyClass()
b = MyClass()

assert a is b
```