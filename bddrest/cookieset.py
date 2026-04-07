from collections import OrderedDict
from typing import Pattern


class CookieSet(OrderedDict):
    def __init__(self, cookies=None):
        super().__init__()

        if not cookies:
            return

        if isinstance(cookies, dict):
            cookies = cookies.items()

        for item in cookies:
            self.append(item)

    def append(self, item, val=None):
        if val:
            self[item] = val
            return

        k, v = item.split('=', 1) if isinstance(item, str) else item
        self[k.strip()] = v.strip()

    def __setitem__(self, k, v):
        k = k.strip()
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
            return super().__contains__(key)

        elif isinstance(key, Pattern):
            for i in self:
                if key.match(i):
                    return True
            return False
        else:
            raise TypeError(f'{type(key)}')
