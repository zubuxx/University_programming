from PIL import Image
import os

def miniature(Original_file, size_of_miniature, new_name, trybe = 0):
    '''

    :param Original_file: str
    ------------------------
    Name of original file with FORMAT

    :param size_of_miniature: int or tuple
    ------------------------
    Size of miniature
    Tuple if the miniature should a rectangle
    If the miniature is to be a square, the parameter can be passed as a int.

    :param new_name: str
    ------------------------
    New name of miniature

    :param trybe: int
    ------------------------
    It takes value of 0 or 1. Default 0.
    If 0, it calculates an appropriate thumbnail size to keep ratio.
    If 1, this option is disabled.

    :return:
    It saves new thumbnail in the folder, where the original image is saved and retruns miniture as a image object.
    '''

    im = Image.open(Original_file)
    thumbnail_format = 'jpg'
    if type(size_of_miniature) == int:
        size_of_miniature = size_of_miniature, size_of_miniature
        if (im.size[0] != im.size[1]) and (trybe==0):
            print('ATTENTION! \nYou want to create a sqaure miniature, but the original image is not a sqaure. To keep ratio between wdith and high the thumbnail will be a rectangle. \nHowever if you want to create a square thumbnail change trybe to 1.')
    if trybe==0:
        im.thumbnail(size_of_miniature, Image.ANTIALIAS)
    else:
        im = im.resize(size_of_miniature, Image.ANTIALIAS)
    if len(os.path.dirname(im.filename))!=0:
        path = os.path.dirname(im.filename) + '/'
    else:
        path=''
    im.save(path + new_name + '.'+thumbnail_format)

    return im


