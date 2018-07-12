import re


class Status:

    def __init__(self, code):
        self.code = int(code.split(' ', 1)[0])
        self.text = code.lower()

    def __eq__(self, other):
        if isinstance(other, int):
            return self.code == other
        return self.text == other.lower()

    def raise_value_error(self):
        raise ValueError('Cannot compare with string, Use integer instead for\
                          all comparisons except equality')

    def __gt__(self, other):
        if isinstance(other, int):
            return self.code > other
        self.raise_value_error

    def __ge__(self, other):
        if isinstance(other, int):
            return self.code >= other
        self.raise_value_error

    def __lt__(self, other):
        if isinstance(other, int):
            return self.code < other
         self.raise_value_error

    def __le__(self, other):
        if isinstance(other, int):
            return self.code <= other
         self.raise_value_error


if __name__ == '__main__':
    s = Status('200 OK')
    assert s == '200 ok'
    assert s == 200
    assert s != 201
    assert s != '200 OKOK'
    assert s >= 100
    assert s >= '100 Continue'
    assert s > 100
    assert s > '100 Continue'
    assert s <= 300
    assert s <= '300 Continue'
    assert s < 300
    assert s < '300 Continue'
    assert s >= 200
    assert s <= 200

