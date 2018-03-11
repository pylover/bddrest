import unittest

from bddrest.specification.common import HeaderSet


class HeaderSetTestCase(unittest.TestCase):

    def test_constructor(self):
        expected_headers = [('A', 'B'), ('C', 'D')]
        headers = HeaderSet(('A: B', 'C: D'))
        self.assertListEqual(expected_headers, headers)

        headers = HeaderSet({'A': 'B', 'C': 'D'})
        self.assertListEqual(expected_headers, headers)

    def test_append(self):
        expected_headers = [('A', 'B'), ('C', 'D')]
        headers = HeaderSet()
        headers.append(('A', 'B'))
        headers.append(('C', 'D'))
        self.assertListEqual(expected_headers, headers)

        headers = HeaderSet()
        headers.append('A: B')
        headers.append('C: D')
        self.assertListEqual(expected_headers, headers)

        headers = HeaderSet()
        headers.append('A', 'B')
        headers.append('C', 'D')
        self.assertListEqual(expected_headers, headers)

    def test_insert(self):
        expected_headers = [('A', 'B'), ('C', 'D')]
        headers = HeaderSet()
        headers.insert(0, ('C', 'D'))
        headers.insert(0, ('A', 'B'))
        self.assertListEqual(expected_headers, headers)

        headers = HeaderSet()
        headers.insert(0, 'C: D')
        headers.insert(0, 'A: B')
        self.assertListEqual(expected_headers, headers)

        headers = HeaderSet()
        headers.insert(0, 'C', 'D')
        headers.insert(0, 'A', 'B')
        self.assertListEqual(expected_headers, headers)

    def test_setitem_getitem_delitem(self):
        expected_headers = [('A', 'B'), ('C', 'D')]
        # setitem
        headers = HeaderSet(['A: F'])
        headers[0] = 'A: B'
        headers['C'] = 'D'
        self.assertListEqual(expected_headers, headers)

        # getitem
        self.assertEqual(expected_headers[0], headers[0])
        self.assertEqual('B', headers['A'])
        self.assertEqual('B', headers['a'])

        # delitem
        del headers[0]
        del headers['C']
        self.assertListEqual([], headers)


if __name__ == '__main__':
    unittest.main()

