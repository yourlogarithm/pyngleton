import unittest

from src.pyngleton import singleton, Singleton, SingletonMeta


class TestSingleton(unittest.TestCase):
    def test_singleton_sequential(self):
        @singleton
        class MySingleton:
            def __init__(self, name):
                self.name = name

        a = MySingleton('a')
        b = MySingleton('b')
        self.assertEqual(a.name, 'a')
        self.assertEqual(b.name, 'a')
        self.assertIs(a, b)

    def test_singleton_class_multithreading(self):
        from concurrent.futures import ThreadPoolExecutor

        @singleton
        class MySingleton:
            def __init__(self, name=None):
                self.name = name

        with ThreadPoolExecutor(max_workers=5) as executor:
            tasks = [executor.submit(MySingleton, i) for i in range(5)]
            singletons = []
            for task in tasks:
                singletons.append(task.result())

        for s in singletons:
            self.assertEqual(0, s.name)

        self.assertEqual(1, len(set(singletons)))

    def test_singleton_class_multiprocessing(self):
        import multiprocessing

        @singleton
        class MySingleton:
            def __init__(self, name, q: multiprocessing.Queue):
                self.name = name
                q.put(name)

        queue = multiprocessing.Queue()

        for i in range(5):
            p = multiprocessing.Process(target=MySingleton, args=(i, queue))
            p.start()
            p.join()

        names = []
        while not queue.empty():
            names.append(queue.get())

        self.assertEqual(5, len(set(names)))

    def test_differences(self):
        @singleton
        class A:
            pass

        @singleton
        class B:
            pass

        a = A()
        b = B()

        self.assertNotEqual(a, b)

    def test_inheriting(self):
        class A(Singleton):
            pass

        class B(metaclass=SingletonMeta):
            pass

        self.assertEqual(A(), A())
        self.assertEqual(B(), B())
        self.assertNotEqual(A(), B())