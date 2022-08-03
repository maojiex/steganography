import hashlib
import os
from PIL import Image
import unittest
from main import decode
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
    
    def test_decode(self):
        script_dir = os.path.dirname(__file__)
        rel_path = '../../test.png'
        abs_img_path = os.path.join(script_dir, rel_path)
        image_to_decode = Image.open(abs_img_path)

        self.assertEqual(decode(image_to_decode, ''), False)
        self.assertEqual(decode(image_to_decode, 'osdfjlj32'), False)
        self.assertEqual(decode(image_to_decode, 'Abcd1234'), False)
        
        password = hashlib.sha256('Abcd1234'.encode()).hexdigest()
        self.assertEqual(decode(image_to_decode, password), 'xyz')

if __name__ == '__main__':
    unittest.main()