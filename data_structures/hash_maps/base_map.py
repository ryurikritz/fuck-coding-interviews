# coding: utf-8
from abc import abstractmethod
from collections.abc import MutableMapping
import random


class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key


class BaseMap(MutableMapping):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def __iter__(self):
        ...

    @abstractmethod
    def __setitem__(self, key, value):
        ...

    @abstractmethod
    def __getitem__(self, key):
        ...

    @abstractmethod
    def __delitem__(self, key):
        ...


class BaseHashMap(BaseMap):
    def __init__(self, capacity=11, load_factor_threshold=0.5, prime=109345121):
        self._bucket_array = [None, ] * capacity  # Setting capacity to a prime number can slightly reduce collision.
        self._size = 0
        self._load_factor_threshold = load_factor_threshold

        # The following variables are used by MAD compression function.
        self._prime = prime
        self._scale = 1 + random.randrange(prime - 1)
        self._shift = random.randrange(prime)

    def __len__(self):
        return self._size

    def _hash_func(self, key):
        """
        We use Python's built-in hash() to generate hash code for key,
        then use Multiply-Add-and-Divide (MAD) as compression function:

        [(hash_code * scale + shift) mod P] mod N

        where N is the size of the bucket array,
        P is a prime number larger than N,
        and scale and shift are random integers from the [0, p – 1], with scale > 0.
        """
        return ((hash(key) * self._scale + self._shift) % self._prime) % len(self._bucket_array)

    def _resize(self, new_capacity):
        old_items = list(self.items())
        self._bucket_array = [None, ] * new_capacity
        self._size = 0
        for key, value in old_items:
            # __setitem__() will re-calculate self._size
            self[key] = value

    def load_factor(self):
        return self._size / len(self._bucket_array)
