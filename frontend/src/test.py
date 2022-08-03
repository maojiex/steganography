import hashlib
import certifi
import urllib
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from PIL import Image
import unittest
from main import decode
from main import validate_password
from main import genData

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
    
    def test_genData(self):
        self.assertEqual(genData("1234"), ['00110001', '00110010', '00110011', '00110100'])
        self.assertEqual(genData("abcd"), ['01100001', '01100010', '01100011', '01100100'])
        self.assertEqual(genData("QWER"), ['01010001', '01010111', '01000101', '01010010'])
        self.assertEqual(genData("!@#$"), ['00100001', '01000000', '00100011', '00100100'])
        self.assertEqual(genData("[];',./"), ['01011011', '01011101', '00111011', '00100111', '00101100', '00101110', '00101111'])

    def test_isConnected(self):
        conn = MongoClient(
            "mongodb+srv://LijuanZhuge:" + urllib.parse.quote(
                "I=myself100%") + "@cluster0.botulzy.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
        try:
            conn.finalproject.command('ismaster')
        except ConnectionFailure:
            print("Server not available")

if __name__ == '__main__':
    unittest.main()