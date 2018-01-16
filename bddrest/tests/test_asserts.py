import unittest

from bddrest import AttributeAssert, RootAssert, AssertionFailed  #, GetItemAssert


class AssertsTestCase(unittest.TestCase):

    def test_full_qualified_name(self):
        class A:
            pass

        root = RootAssert(A, 'obj')
        self.assertEqual('obj.a.b.c.d', root.a.b.c.d.get_full_qualified_name())

    def test_attribute_assert(self):

        class A:
            class B:
                c = 12

        root = RootAssert(A, 'obj')
        self.assertIsInstance(root.B, AttributeAssert)
        self.assertIsInstance(root.B.c, AttributeAssert)
        self.assertIsInstance(root.missing_attribute, AttributeAssert)

        self.assertIs(root.B.resolve(), A.B)
        self.assertEqual(root.B.c.resolve(), 12)
        self.assertRaises(root.missing_attribute.resolve(), AssertionFailed)

    # def test_getitem_assert(self):
    #
    #     class A:
    #         b = dict(c=12)
    #
    #     root = RootAssert(A)
    #     self.assertIsInstance(root.b, AttributeAssert)
    #     self.assertIsInstance(root.b['c'], GetItemAssert)
    #     self.assertIsInstance(root.b['missing_item'], GetItemAssert)
    #
    #     self.assertIs(root.B.resolve(), A.B)
    #     self.assertEqual(root.B.c.resolve(), 12)



if __name__ == '__main__':
    unittest.main()
