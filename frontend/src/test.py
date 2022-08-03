import unittest

from main import validate_password

class Testing(unittest.TestCase):
    def test_validate_password(self):
        self.assertEqual(validate_password(''), 0)
        self.assertEqual(validate_password('Abc123'), 0)
        self.assertEqual(validate_password('Abc123Abc123Abc123Abc123'), 0)
        self.assertEqual(validate_password('AAAAAAAA'), 1)
        self.assertEqual(validate_password('AAAAbbbbc'), 1)
        self.assertEqual(validate_password('123456789'), 2)
        self.assertEqual(validate_password('AAAA12345'), 2)
        self.assertEqual(validate_password('aaaa12345'), 3)
        self.assertEqual(validate_password('5we13aaaa12345'), 3)
        self.assertEqual(validate_password('AAAaaaa12345'), -1)
        self.assertEqual(validate_password('kjs36adfjIS230Rcv5D'), -1)

if __name__ == '__main__':
    unittest.main()