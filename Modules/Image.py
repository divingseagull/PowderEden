from PIL import Image


def make_map_image(size, background, pixels: dict):
    """
    :requirements: pillow

    args 인자에서 색상, 위치를 받아서 이미지를 생성함

    size = (x, y)

    background = (R, G, B)

    pixels = {
        (R, G, B): [
            (x, y),
            ...
        ],
        ...
    }
    """

    img = Image.new(mode="RGB", size=(size[0], size[1]), color=background)

    for rgb in pixels:
        for xy in pixels[rgb]:
            img.putpixel(xy, rgb)

    return img
