import unittest
import re

from bddrest.specification.headerset import HeaderSet


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

    def test_in_operator(self):
        headers = HeaderSet(['A: F'])
        self.assertIn('A', headers)
        self.assertIn('a', headers)
        self.assertIn('A: F', headers)

    def test_extend(self):
        expected_headers = [('A', 'B'), ('C', 'D')]

        headers = HeaderSet(['A: B'])
        headers.extend(['C: D'])
        self.assertListEqual(expected_headers, headers)

    def test_regex_match(self):
        headers = HeaderSet(['Content-Type: application/json;utf-8'])
        self.assertIn(re.compile('^content-type: .*', re.I), headers)

    def test_remove(self):
        headers = HeaderSet([('A', 'B'), ('C', 'D')])
        headers.remove('A')
        headers.remove('C: D')
        self.assertListEqual([], headers)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

