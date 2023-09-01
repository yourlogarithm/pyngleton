Thread-safe and process-safe singleton class.
The singleton is shared between all threads.
For every process, a new instance is initialized and shared between all threads of the process.

## Examples
### Basic usage:
```python
from pyngleton import singleton

@singleton
class MyClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

if __name__ == '__main__':
    a = MyClass(1, 2, 3)
    b = MyClass(4, 5, 6)
    
    assert a is b
    
    assert b.x == 1 and b.y == 2 and b.z == 3
```

### Multithreading:
```python
from concurrent.futures import ThreadPoolExecutor
from pyngleton import singleton
   
@singleton
class MyClass:
    pass

if __name__ == '__main__':
    n = 2
    with ThreadPoolExecutor(max_workers=n) as exc:
        tasks = [exc.submit(MyClass) for _ in range(n)]
        results = set(task.result() for task in tasks)
    assert len(results) == 1  # all threads share the same instance
```

### Multiprocessing:
```python
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from pyngleton import singleton

@singleton
class MyClass:
    def __init__(self, x: int, y: int, z: int, queue: multiprocessing.Queue):
        self.x = x
        self.y = y
        self.z = z
        queue.put((x, y, z))
        
def worker(x: int, y: int, z: int, queue: multiprocessing.Queue):
    MyClass(x, y, z, queue)

if __name__ == '__main__':
    n = 2
    queue = multiprocessing.Manager().Queue()
    with ProcessPoolExecutor(max_workers=n) as exc:
        tasks = [exc.submit(worker, i, i, i, queue) for i in range(n)]
        for task in tasks:
            task.result()
    results = []
    while not queue.empty():
        results.append(queue.get())
    assert results == [(0, 0, 0), (1, 1, 1)]  # each process has its own instance
```
The classes decorated with `@singleton` can't be pickled. If you want to be able to do that, 
you can inherit from `Singleton` or `SingletonMeta` instead of using the decorator.

### Inheriting:
```python
from pyngleton import Singleton, SingletonMeta

class MyClassA(metaclass=SingletonMeta):
    pass

class MyClassB(Singleton):
    pass
    
if __name__ == '__main__':
    assert MyClassA() is MyClassA()
    assert MyClassB() is MyClassB()
    assert MyClassA() is not MyClassB()
```