from tabnanny import check
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import SaveFileDialog
from click import command
import io
import os
from cryptography.fernet import Fernet
import PySimpleGUI as sg

import hashlib
from PIL import Image
import bson
from gridfs import validate_string
import pymongo
import requests
import urllib
import certifi


# PIL module is used to extract pixels of image and modify it
from PIL import Image, ImageTk

file_types = [("PNG (*.png)", "*.png"),
			  ("JPEG (*.jpg)", "*.jpg"),
			  ("All files (*.*)", "*.*")]


# Convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
	# list of binary codes of given data
	newd = []

	for i in data:
		newd.append(format(ord(i), '08b'))
	return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
			   imdata.__next__()[:3] +
			   imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if datalist[i][j] == '0' and pix[j] % 2 != 0:
				pix[j] -= 1

			elif datalist[i][j] == '1' and pix[j] % 2 == 0:
				if pix[j] != 0:
					pix[j] -= 1
				else:
					pix[j] += 1
			# pix[j] -= 1

		# Eighth pixel of every set tells whether to stop ot read further.
		# 0 means keep reading; 1 means the message is over.
		if i == lendata - 1:
			if pix[-1] % 2 == 0:
				if pix[-1] != 0:
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if pix[-1] % 2 != 0:
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]


def encode_enc(new_img, data):
	w = new_img.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(new_img.getdata(), data):

		# Putting modified pixels in the new image
		new_img.putpixel((x, y), pixel)
		if x == w - 1:
			x = 0
			y += 1
		else:
			x += 1


# Encode data into image
def encode(image, data, password):
	if len(data) == 0:
		raise ValueError('Data is empty')

	data = password + data
	new_img = image.copy()
	encode_enc(new_img, data)
	return new_img


# Decode the data in the image
def decode(image, password):

	data = ''
	imgdata = iter(image.getdata())

	while True:
		pixels = [value for value in imgdata.__next__()[:3] +
				  imgdata.__next__()[:3] +
				  imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if i % 2 == 0:
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if pixels[-1] % 2 != 0:
			existing_password = data[:64]
			print('password check:',password, existing_password)
			if password == existing_password:
				return data[64:]
			else:
				return False

def db_operations(image, encode_message, password):
    conn = pymongo.MongoClient(
        "mongodb+srv://LijuanZhuge:" + urllib.parse.quote(
            "US-65&sR@P5A#@F") + "@cluster0.botulzy.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = conn.finalproject
    inserted_id = db.encoderecords.insert_one({"file": [{"encoded_img": bson.binary.Binary(image.getvalue())},{'encode_message':encode_message},{"password":password}]}).inserted_id
    return inserted_id

def db_searching(id):
	conn = pymongo.MongoClient(
		"mongodb+srv://LijuanZhuge:" + urllib.parse.quote(
			"US-65&sR@P5A#@F") + "@cluster0.botulzy.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
	db = conn.finalproject
	if db.encoderecords.count_documents({"_id":bson.ObjectId(id)}) > 0:
		return True
	return False

def is_valid_key(oid):
        if not oid:
            return False

        try:
            bson.ObjectId(oid)
            return True
        except (bson.errors.InvalidId, TypeError):
            return False 

def validate_password(password):
    # length of password must be between [8, 20]
    # password must contain at least one digit
    # password must contain at least one lower case character
    # password must contain at least one upper case character
    # length, digit, lower, upper
    checks = [False] * 4

    if len(password) >= 8 and len(password) <= 20:
        checks[0] = True
    
    for char in password:
        if char.isdigit():
            checks[1] = True
        elif char.islower():
            checks[2] = True
        elif char.isupper():
            checks[3] = True
    
    for i in range(len(checks)):
        if not checks[i]:
            return i
	
    return -1

def encrypt(message):
	# generate a key for encryption and decryption
	key = Fernet.generate_key()
	# Instance the Fernet class with the key
	fernet = Fernet(key)
	# then use the Fernet class instance
	# to encrypt the string string must
	# be encoded to byte string before encryption
	encMessage = fernet.encrypt(message.encode())

	print("original string: ", message)
	print("encrypted string: ", encMessage)
	return encMessage, key

def decrypt(encMessage, key):
	# decrypt the encrypted string with the
	# Fernet instance of the key,
	# that was used for encrypting the string
	# encoded byte string is returned by decrypt method,
	# so decode it to string with decode methods

	# Instance the Fernet class with the key
	fernet = Fernet(key)

	decMessage = fernet.decrypt(encMessage).decode()

	print("decrypted string: ", decMessage)
	return decMessage

# Main Function
def main():
	layout = [
		[sg.Image(key="-IMAGE-", size=(50, 1)), sg.Image(key="-IMAGEAFTER-", size=(50, 1))],
		[sg.Text(key="imagetag", size=(30, 1)), sg.Text(key="imagetag_after", size=(30, 1))],
        [sg.Text("You can encode Here: ", size = (50,1),font=('Helvetica', 15),text_color='blue')],
		[
			sg.Text("Image File"),
			sg.Input(size=(25, 1), key="-FILE-"),
			sg.FileBrowse(file_types=file_types),
			sg.Button("Load Image"),
		],
		[
			sg.Text("Encode Message"),
			sg.Multiline(size=(15, 2), key="-Encode Message-"),
		],
		[
			sg.Text("Password"),
			sg.InputText(size=(15, 2), password_char='*', key="-Encode Password-"),
		],
		[
			sg.Text("Type Eecoded Image Name"),
		 	sg.InputText(size=(15, 2), key="-New Name-"), 
		 	sg.Button("Encode and Download"),
		],
        [sg.Text("You can decode Here: ", size = (50,1),font=('Helvetica', 15),text_color='blue')],
        [sg.Image(key="-IMAGEtobedecoded-", size=(50, 1))],
        [
			sg.Text("Image to Decode"),
			sg.Input(size=(25, 1), key="-Encoded FILE-"),
			sg.FileBrowse(file_types=file_types),
			sg.Button("Input Image"),
		],		
		[sg.Text("Enter the Database Insert id"), sg.Input(size=(30,2), key="-Key-"),sg.Text("hint : the inserted_id when image are uploaded to database",font=('Helvetica',10))],
		[sg.Text("Enter the encode key"), sg.Input(size=(30, 2), key="-Keynew-"),],

		[
			sg.Text("Enter Password to Decode"),
			sg.InputText(size=(15, 2), password_char='*', key="-Decode Password-"),
			sg.Button("Decode"),
		],
		[
			sg.Text("Decoded Message"),
			sg.Multiline(size=(15, 2), key="-Decoded Message-"),
		]
	]

	window = sg.Window("Image Viewer", layout)

	image_upload_flag = False
	encoded_upload_flag = False
	while True:

		event, values = window.read()
		
		if event == "Exit" or event == sg.WIN_CLOSED:
			break

		if event == "Load Image":
			filename = values["-FILE-"]
			if os.path.exists(filename):
				image = Image.open(values["-FILE-"])
				image_upload_flag = True
				image.thumbnail((150, 150))

				bio = io.BytesIO()
				image.save(bio, format="PNG")
				window["-IMAGE-"].update(data=bio.getvalue())

		if event == "Encode and Download":
			if image_upload_flag == False:
				sg.popup('No image uploaded, please upload an image first')
				continue
			encode_message = values["-Encode Message-"]
			if len(encode_message) == 0:
				sg.popup('No encode message provided')
				continue
			#add plain text encrypt
			encrypt_message, keygenerate = encrypt(encode_message)

			ori_password = values['-Encode Password-']
			if len(ori_password) == 0:
				sg.popup('No password provided')
				continue
            # validate password
			validate_res = validate_password(ori_password)
			if validate_res == 0:
				sg.popup('Length of password must be between 8 and 20')
				continue
			elif validate_res == 1:
				sg.popup('Password must contain at least one digit')
				continue
			elif validate_res == 2:
				sg.popup('Password must contain at least one lower case character')
				continue
			elif validate_res == 3:
				sg.popup('Password must contain at least one upper case character')
				continue
			if len(values["-New Name-"]) == 0:
				sg.popup("Please Create A New Image Name")
				continue
			password = hashlib.sha256(ori_password.encode()).hexdigest()
			print('encrypt str:',encrypt_message.decode('ascii'))
			new_image = encode(image, encrypt_message.decode('ascii'), password)
			new_image.copy().save(values["-New Name-"] + ".png")

			# image_decoded = True
			new_bio = io.BytesIO()
			new_image.save(new_bio, format="PNG")
			window['-IMAGEAFTER-'].update(data=new_bio.getvalue())
			window["imagetag"].update("Original Image")
			window["imagetag_after"].update("Image Encoded")
			# save encoded image into database
			inserted_id = db_operations(new_bio, encode_message, password)
			sg.popup('image encoded successfully, saved in database, please write down the key to decode: ' + str(inserted_id) +"\n"+ "key:"+keygenerate.decode('ascii'))
			print('insert_id:',str(inserted_id))
			print('key:',keygenerate.decode('ascii'))


		if event == "Input Image":
			filename = values["-Encoded FILE-"]
			if os.path.exists(filename):
				image_to_decode = Image.open(values["-Encoded FILE-"])
				encoded_upload_flag = True
				image_to_decode.thumbnail((150, 150))
				bio = io.BytesIO()
				image_to_decode.save(bio, format="PNG")
				window["-IMAGEtobedecoded-"].update(data=bio.getvalue())

		if event == "Decode":
			if encoded_upload_flag == False:
				sg.popup('No encoded image uploaded')
				continue

			input_key = values['-Key-']
			password = values['-Decode Password-']
			keynew = values['-Keynew-']
      
			if is_valid_key(input_key) == False:
				sg.popup("Not a valid Key")
				continue
			if db_searching(input_key) == False:
				sg.popup('Key is not existing')
				continue
			else:
				pass

			if len(password) == 0:
				sg.popup('No password entered')
				continue

			password = hashlib.sha256(password.encode()).hexdigest()
			decode_result = decode(image_to_decode, password)

			if decode_result == False:
				sg.popup('Incorrect password')
				continue

			# get ori encode message from decryption
			decryption_message = decrypt(decode_result.encode('ascii'), keynew.encode('ascii'))

			window["-Decoded Message-"].update(decryption_message)
	window.close()


# Driver Code
if __name__ == '__main__':
	main()



