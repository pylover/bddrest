

class A:
    def __enter__(self):
        print('A.__enter__')
        return B()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('A.__exit__')


class B:
    pass


if __name__ == '__main__':
    with A() as b:
        print('Nothing', b)
