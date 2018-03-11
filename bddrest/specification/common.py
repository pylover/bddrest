from collections import Iterable


class HeaderSet(list):
    def __init__(self, headers=None):
        if headers:
            if isinstance(headers, dict):
                headers = list(headers.items())

            super().__init__(self._normalize_item(i) for i in headers)
        else:
            super().__init__()

    def _normalize_item(self, h):
        k, v = h.split(':', 1) if isinstance(h, str) else h
        return k, v.strip()

    def append(self, k, v=None):
        if v:
            return super().append((k, v))
        else:
            return super().append(self._normalize_item(k))


