import unittest

from bddrest import AssertAttribute, AssertRoot, AssertionFailed, AssertGetItem, AssertComparison


class AssertsTestCase(unittest.TestCase):

    def test_full_qualified_name(self):
        class A:
            pass

        root = AssertRoot(A, 'obj')
        self.assertEqual('obj.a.b.c.d', root.a.b.c.d.__str__())

    def test_attribute_assert(self):
        class A:
            class B:
                c = 12

        root = AssertRoot(A)
        self.assertIsInstance(root.B, AssertAttribute)
        self.assertIsInstance(root.B.c, AssertAttribute)
        self.assertIsInstance(root.missing_attribute, AssertAttribute)

        self.assertIs(root.B.resolve(), A.B)
        self.assertEqual(root.B.c.resolve(), 12)
        with self.assertRaises(AssertionFailed) as c:
            root.missing_attribute.resolve()
        self.assertEqual(
            f'\nAssertion Failed:\n'
            f'Object: target has no attribute missing_attribute',
            str(c.exception)
        )

    def test_getitem_assert(self):
        class B:
            f = 4
            pass

        class A:
            b = dict(c=12)
            k = [1, 2, dict(a=2, b=B())]

        root = AssertRoot(A)
        self.assertIsInstance(root.b, AssertAttribute)
        self.assertIsInstance(root.b['c'], AssertGetItem)
        self.assertIsInstance(root.b['missing_item'], AssertGetItem)

        self.assertEqual(root.b['c'].resolve(), 12)
        self.assertEqual(root.k[0].resolve(), 1)
        self.assertEqual(root.k[:2].resolve(), [1, 2])
        self.assertEqual(root.k[2]['a'].resolve(), 2)
        self.assertEqual(root.k[2]['b'].f.resolve(), 4)

        self.assertEqual('target.b[\'c\']', root.b['c'].__str__())
        self.assertEqual('target.k[0]', root.k[0].__str__())
        self.assertEqual('target.k[:2]', root.k[:2].__str__())
        self.assertEqual('target.k[1:2]', root.k[1:2].__str__())
        self.assertEqual('target.k[::2]', root.k[::2].__str__())

        with self.assertRaises(AssertionFailed) as c:
            root.b['missing'].resolve()
        self.assertEqual(
            f'\nAssertion Failed:\n'
            f'Object: target.b has no item missing',
            str(c.exception)
        )

        with self.assertRaises(AssertionFailed) as c:
            root.k[9999].resolve()
        self.assertEqual(
            f'\nAssertion Failed:\n'
            f'Object: target.k has no item 9999',
            str(c.exception)
        )

    def test_assert_equal(self):
        class A:
            f = 4

        target = AssertRoot(A)
        self.assertIsInstance(target.f == 4, AssertComparison)
        self.assertIsInstance(target.f == 3, AssertComparison)
        self.assertTrue((target.f == 4).resolve())
        self.assertEqual('target.f == 4', str(target.f == 4))

        with self.assertRaises(AssertionFailed) as c:
            (target.f == 3).resolve()
        self.assertEqual(
            '\nThe expression:\n\n\ttarget.f == 3\n\n'
            'has been failed.\n'
            'Expected: 3\n'
            'Actual: 4',
            str(c.exception)
        )

    def test_assert_not_equal(self):
        class A:
            f = 3

        target = AssertRoot(A)
        self.assertIsInstance(target.f != 4, AssertComparison)
        self.assertIsInstance(target.f != 3, AssertComparison)
        self.assertTrue((target.f != 4).resolve())
        self.assertEqual('target.f != 4', str(target.f != 4))
        with self.assertRaises(AssertionFailed) as c:
            (target.f != 3).resolve()
        self.assertEqual(
            '\nThe expression:\n\n\ttarget.f != 3\n\n'
            'has been failed.\n'
            'Not Expected: 3\n'
            'Actual: 3',
            str(c.exception)
        )

    def test_assert_greater_than(self):
        class A:
            f = 4

        target = AssertRoot(A)
        self.assertIsInstance(target.f > 3, AssertComparison)
        self.assertTrue((target.f > 3).resolve())
        self.assertEqual('target.f > 4', str(target.f > 4))
        with self.assertRaises(AssertionFailed) as c:
            (target.f > 4).resolve()
        self.assertEqual(
            '\nThe expression:\n\n\ttarget.f > 4\n\n'
            'has been failed.\n',
            str(c.exception)
        )

    def test_assert_greater_than_equal(self):
        class A:
            f = 4

        target = AssertRoot(A)
        self.assertIsInstance(target.f >= 3, AssertComparison)
        self.assertTrue((target.f >= 4).resolve())
        self.assertEqual('target.f >= 4', str(target.f >= 4))
        with self.assertRaises(AssertionFailed) as c:
            (target.f >= 9).resolve()
        self.assertEqual(
            '\nThe expression:\n\n\ttarget.f >= 9\n\n'
            'has been failed.\n',
            str(c.exception)
        )

    def test_assert_lesser_than(self):
        class A:
            f = 4

        target = AssertRoot(A)
        self.assertIsInstance(target.f < 3, AssertComparison)
        self.assertTrue((target.f < 5).resolve())
        self.assertEqual('target.f < 4', str(target.f < 4))
        with self.assertRaises(AssertionFailed) as c:
            (target.f < 4).resolve()
        self.assertEqual(
            '\nThe expression:\n\n\ttarget.f < 4\n\n'
            'has been failed.\n',
            str(c.exception)
        )

    def test_assert_lesser_than_equal(self):
        class A:
            f = 4

        target = AssertRoot(A)
        self.assertIsInstance(target.f <= 3, AssertComparison)
        self.assertTrue((target.f <= 4).resolve())
        self.assertEqual('target.f <= 4', str(target.f <= 4))
        with self.assertRaises(AssertionFailed) as c:
            (target.f <= 3).resolve()
        self.assertEqual(
            '\nThe expression:\n\n\ttarget.f <= 3\n\n'
            'has been failed.\n',
            str(c.exception)
        )


if __name__ == '__main__':
    unittest.main()
