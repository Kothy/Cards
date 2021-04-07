from PIL import Image
import unicodedata


def resize_image(img, max_width, max_height):
    max_width = int(max_width)
    max_height = int(max_height)
    w_percent = (max_width / float(img.size[0]))
    height = int((float(img.size[1]) * float(w_percent)))
    if height > max_height:
        wpercent = (max_height / float(img.size[1]))
        width = int((float(img.size[0]) * float(wpercent)))
        return img.resize((width, max_height), Image.ANTIALIAS)
    return img.resize((max_width, height), Image.ANTIALIAS)


def resize_image_by_width(img, basewidth):
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def resize_image_by_height(img, hsize):
    wpercent = (hsize / float(img.size[1]))
    basewidth = int((float(img.size[0]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def strip_accents_list(arr):
    result = list()
    for item in arr:
        result.append(strip_accents(item))
    return result
