import os
import threading


def singleton(cls):
    """
    Decorator for declaring the class as a thread-safe & process-safe singleton.
    """
    instances = {}
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        key = (os.getpid(), cls.__name__)
        if key not in instances:
            with lock:
                if key not in instances:
                    instances[key] = cls(*args, **kwargs)
        return instances[key]
    return wrapper


class SingletonMeta(type):
    """
    This is a metaclass that creates a Singleton instance. It creates the instance in a
    process-safe and thread-safe manner.
    """

    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        This method is called when the class is instantiated. It creates a Singleton instance
        if it doesn't exist.
        """

        key = (os.getpid(), cls.__name__)
        if key not in cls._instances:
            with cls._lock:
                if key not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[key] = instance
        return cls._instances[key]


class Singleton(metaclass=SingletonMeta):
    """
    This is the Singleton class that uses the SingletonMeta metaclass. It should be inherited by any class
    that should be a Singleton.
    """


__all__ = ['singleton', 'Singleton', 'SingletonMeta']
