import unittest

from bddrest import AssertAttribute, AssertRoot, AssertionFailed, AssertGetItem, AssertComparison


class AssertsTestCase(unittest.TestCase):

    def test_full_qualified_name(self):
        class A:
            pass

        root = AssertRoot(A, 'obj')
        self.assertEqual('obj.a.b.c.d', root.a.b.c.d.get_full_qualified_name())

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
        self.assertRaises(AssertionFailed, root.missing_attribute.resolve)

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

        self.assertEqual(root.b['c'].get_full_qualified_name(), 'target.b[\'c\']')
        self.assertEqual(root.k[0].get_full_qualified_name(), 'target.k[0]')
        self.assertEqual(root.k[:2].get_full_qualified_name(), 'target.k[:2]')
        self.assertEqual(root.k[1:2].get_full_qualified_name(), 'target.k[1:2]')
        self.assertEqual(root.k[::2].get_full_qualified_name(), 'target.k[::2]')

        self.assertRaises(AssertionFailed, root.b['missing'].resolve)
        self.assertRaises(AssertionFailed, root.k[9999].resolve)

    def test_assert_equal(self):

        class A:
            f = 4

        root = AssertRoot(A)
        self.assertIsInstance(root.f == 4, AssertComparison)
        self.assertIsInstance(root.f == 3, AssertComparison)
        self.assertTrue((root.f == 4).resolve())
        self.assertRaises(AssertionFailed, (root.f == 3).resolve)


if __name__ == '__main__':
    unittest.main()
