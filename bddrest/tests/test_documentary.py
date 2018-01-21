import unittest
from bddrest import generate_documents


class DocumentaryTestCase(unittest.TestCase):

    def test_markdown_generator(self):
        generate_documents('data')


if __name__ == '__main__':
    unittest.main()
