# from PIL import Image

# def crop_and_resize(img, msg, (100, 100)):

#     img =Image.open(img)
#     if img != "JPEG":
#         return (False, "FIle is not a JPEG", None)
#     orig_size = img.size
#     #tuple
# #height
#     orig_size = img.orig_sizeif orig_size[0] > 5000 or orig_size[0] < 5:
#         return (Flase, "too small", None)
# #width
#     orig_size = img.orig_sizeif orig_size[1] > 5000 or orig_size[1] < 5:
#         return (Flase, "too small", None)

#     smallest_side = min(orig_size[0], orig_size[1])

#     #width greatere than height

#     if orig_size[0] > orig_size[1]:
#         y = (orig_size[1] - smallest_side) / 2

#         new_size = (0, 0, x + smallest_side, smallest_side)

#     #height greater than width

#     if orig_size[0] < orig_size[1]:
#         x = (orig_size[1] - smallest_side) / 2

#         new_size = (0, 0, x + smallest_side, smallest_side)

#     # width same as heihgt
#         new_size = (x, 0, x + smallest_side, original_size[1])
     
from PIL import Image


def resize_image_square_crop(src_img_stream, required_size=(100, 100)):
    """
    returns (bool, msg, img)
    """
    img = Image.open(src_img_stream)
    if img.format != "JPEG":
        return (False, "File is not JPEG", None)

    original_size = img.size
    if original_size[0] > 5000 or original_size[0] < 5:
        return (False, "Image size too big or small", None)

    if original_size[1] > 5000 or original_size[1] < 5:
        return (False, "Image size too big or small", None)

    smallest_side = min(original_size[0], original_size[1])

    if original_size[0] > original_size[1]:
        x = (original_size[0] - smallest_side) / 2
        new_size = (x, 0, x + smallest_side, original_size[1])
    elif original_size[0] < original_size[1]:
        y = (original_size[1] - smallest_side) / 2
        new_size = (0, y, smallest_side, y + smallest_side)
    else:
        new_size = (0, 0, smallest_side, smallest_side)

    cropped_image = img.crop(new_size)
    resize_image = cropped_image.resize(required_size)
    return (True, "Resized the image", resize_image)


def resize_image(src_img_stream, required_size=(100, 100)):
    """
    returns (bool, msg, img)
    """
    img = Image.open(src_img_stream)
    if img.format != "JPEG":
        return (False, "File is not JPEG", None)

    original_size = img.size
    if original_size[0] > 5000 or original_size[0] < 5:
        return (False, "Image size too big or small", None)

    if original_size[1] > 5000 or original_size[1] < 5:
        return (False, "Image size too big or small", None)

    # smallest_side = min(original_size[0], original_size[1])

    # if original_size[0] > original_size[1]:
    #     x = (original_size[0] - smallest_side) / 2
    #     new_size = (x, 0, x + smallest_side, original_size[1])
    # elif original_size[0] < original_size[1]:
    #     y = (original_size[1] - smallest_side) / 2
    #     new_size = (0, y, smallest_side, y + smallest_side)
    # else:
    #     new_size = (0, 0, smallest_side, smallest_side)

    # cropped_image = img.crop(new_size)
    resize_image = img.resize(required_size)
    return (True, "Resized the image", resize_image)