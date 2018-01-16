import unittest

from bddrest.asserts import AttributeAssert, RootAssert


class AssertsTestCase(unittest.TestCase):
    def test_attribute_assert(self):

        class A:
            class B:
                c = 12

        root = RootAssert(A)
        self.assertIsInstance(root.B, AttributeAssert)
        self.assertIsInstance(root.B.c, AttributeAssert)
        self.assertIsInstance(root.not_extance, AttributeAssert)


if __name__ == '__main__':
    unittest.main()
