import os
import threading


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

        pid = os.getpid()
        if pid not in cls._instances:
            with cls._lock:
                if pid not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[pid] = instance
        return cls._instances[pid]


class Singleton(metaclass=SingletonMeta):
    """
    This is the Singleton class that uses the SingletonMeta metaclass. It should be inherited by any class
    that should be a Singleton.
    """
    pass

    @classmethod
    def reset(cls):
        with cls._lock:
            cls._instances.clear()


__all__ = ['Singleton', 'SingletonMeta']
