from tkinter import *
import eel
import io
import os
import PySimpleGUI as sg
from PIL import Image

# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image, ImageTk

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]



# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
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

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
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
@eel.expose
def encode(image, data):
    # img = input("Enter image name(with extension) : ")
    # image = Image.open("./input_img/" + img, 'r')

    # data = input("Enter data to be encoded : ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    new_img = image.copy()
    encode_enc(new_img, data)

    # new_img_name = input("Enter the name of new image(with extension) : ")
    # new_img.save("./output_img/" + new_img_name, str(new_img_name.split(".")[1].upper()))
    # GUI_encode(new_img)
    return new_img

# Decode the data in the image
def decode(image):
    # img = input("Enter image name(with extension) : ")
    # image = Image.open("./output_img/" + img, 'r')

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
            return data

@eel.expose
def GUI_decode(input_str):
    root = Tk()
    Label(root, text=input_str).pack()
    root.title("decoding the message")
    root.mainloop()


def GUI_encode(img):
    root = Tk()
    root.title("encoded image")
    GUI_img = ImageTk.PhotoImage(img)
    Label(image=GUI_img).pack()
    root.mainloop()


# Main Function
@eel.expose
def main():

    layout = [
        [sg.Image(key="-IMAGE-"), sg.Image(key="-IMAGEAFTER-")],
        [sg.Text(key="imagetag",size = (50,1)), sg.Text(key="imagetag_after", size = (50,1))],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
        [
            sg.Text("Encode Message"),
            sg.Multiline(size=(15, 2), key="-Encode Message-"),
            sg.Button("Encode"),
        ],
        [
            sg.Button("Decode"),
            sg.Text("Decoded Message"),
            sg.Multiline(size=(15, 2), key="-Decoded Message-"),
        ]
    ]

    window = sg.Window("Image Viewer", layout)

    image_upload_flag = False
    image_decoded = False
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image_upload_flag = True
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
        if event == "Encode":
            if image_upload_flag == False:
                sg.popup('No image uploaded, please upload an image at first')
                continue
            encode_message = values["-Encode Message-"]
            if len(encode_message) == 0:
                sg.popup('No encode message are provided')
                continue
            new_image = encode(image,encode_message)
            image_decoded = True
            new_bio = io.BytesIO()
            new_image.save(new_bio, format="PNG")
            window['-IMAGEAFTER-'].update(data = new_bio.getvalue())
            window["imagetag"].update("Original Image")
            window["imagetag_after"].update("Image Encoded")
        if event == "Decode":
            if image_decoded == False:
                sg.popup('Image are not encoded, please encode first')
                continue
            decode_result = decode(new_image)
            window["-Decoded Message-"].update(decode_result)

    window.close()



# Driver Code
if __name__ == '__main__':
    # Calling main function
    main()
