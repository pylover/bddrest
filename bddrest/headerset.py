from collections import OrderedDict
from typing import Pattern


class HeaderSet(OrderedDict):
    def __init__(self, headers=None):
        super().__init__()

        if not headers:
            return

        if isinstance(headers, dict):
            headers = headers.items()

        for item in headers:
            self.append(item)

    def append(self, item, val=None):
        if val:
            self[item] = val
            return

        k, v = item.split(':', 1) if isinstance(item, str) else item
        self[k] = v

    def __setitem__(self, k, v):
        k = k.strip().lower()
        val = self.get(k)
        if val:
            val += f',{v.strip()}'
        else:
            val = v.strip()

        super().__setitem__(k, val)

    def tostrlist(self):
        return [f'{k}: {v}' for k, v in self.items()]

    def __contains__(self, key):
        if isinstance(key, str):
            return super().__contains__(key.lower())

        elif isinstance(key, Pattern):
            for i in self:
                if key.match(i):
                    return True
            return False
        else:
            raise TypeError(f'{type(key)}')
