from PIL import Image, ImageDraw
import Main

def makeGrid(
    image: Image.Image,
    sizeX: int,
    sizeY: int,
    gridAmountX: int,
    gridAmountY: int,
    # smoothGridY: bool=True,
    # **options
    ) -> ImageDraw.ImageDraw:

    draw = ImageDraw.ImageDraw(image)
    gridDistanceX = sizeX // gridAmountX
    gridDistanceY = sizeY // gridAmountY

    for i in range(1, gridAmountX + 1):
        draw.line(
            [(), ()], # 수정 필요
            width=1
        )
    
    for ii in range(1, gridAmountY + 1):
        draw.line(
            [(), ()], # 수정 필요
            width=1
        )

    return draw

img = Image.new("RGB", (99, 99), 'Black')
makeGrid(img, 99, 99, 99, 99)
img.save(f"{Main.path}/Data/Image/TestImage.png")
