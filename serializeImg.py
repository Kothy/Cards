from PIL import Image
import io
import json


def imageToBytes2(path):
    im = Image.open(path)
    buf = io.BytesIO()
    im.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im


def textToBytes(image):
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im


def toJson(byts, path):
    d = dict()
    d["image"] = byts.decode("latin_1")
    with open(path, "w") as write_file:
        json.dump(d, write_file)


def bytesToString(byts):
    return byts.decode("latin_1")


def fromJson(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
    b = data["image"]
    b = b.encode("latin_1")
    return b


def imageToText(image):
    b = textToBytes(image) # image je vo formate Image
    return bytesToString(b)  # vrati textovu reprezentaciu obrazku

def textToImage(text):
    by = text.encode("latin_1")
    img = Image.open(io.BytesIO(by))
    return img

