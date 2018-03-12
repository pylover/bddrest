import re
from typing.re import Pattern

from collections import Iterable


class HeaderSet(list):
    def __init__(self, headers=None):
        if headers:
            if isinstance(headers, dict):
                headers = list(headers.items())

            super().__init__(self._normalize_item(i) for i in headers)
        else:
            super().__init__()

    @staticmethod
    def _normalize_item(h):
        k, v = h.split(':', 1) if isinstance(h, str) else h
        return k, v.strip()

    @property
    def simple(self):
        return [f'{k}: {v}' for k, v in self]

    def _get_item_by_key(self, key):
        testkey = key.casefold()
        if ':' in key:
            for i, h in enumerate(self.simple):
                if testkey == h.casefold():
                    k, v = self[i]
                    return i, k, v
        else:
            for i, (k, v) in enumerate(self):
                if k.casefold() == testkey:
                    return i, k, v

        raise KeyError(key)

    def append(self, k, v=None):
        if v:
            return super().append((k, v))
        else:
            return super().append(self._normalize_item(k))

    def insert(self, i, k, v=None):
        if v:
            return super().insert(i, (k, v))
        else:
            return super().insert(i, self._normalize_item(k))

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.append(key, value)
        else:
            super().__setitem__(key, self._normalize_item(value))

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._get_item_by_key(key)[2]
        else:
            return super().__getitem__(key)

    def __delitem__(self, key):
        if isinstance(key, str):
            super().__delitem__(self._get_item_by_key(key)[0])
        else:
            super().__delitem__(key)

    def __contains__(self, key):
        if isinstance(key, str):
            try:
                self._get_item_by_key(key)
                return True
            except KeyError:
                return False
        elif isinstance(key, Pattern):
            for i in self.simple:
                if key.match(i):
                    return True
            return False
        else:
            return super().__contains__(key)

    def extend(self, other):
        super().extend(self._normalize_item(i) for i in other)

    def remove(self, key):
        if isinstance(key, str):
            key = self._get_item_by_key(key)[1:]
        super().remove(key)

