from PIL import Image
from tkinter import filedialog, Tk


def difference(value1, value2):
    "Compute difference between two pixels value"
    a = abs(value1 - value2)
    if a > 255:
        a = a - 255
    else:
        pass
    return int(a)

def create_image(i, j, colour):
    """
    Create image with given width , height and colour
    :param i: width
    :param j:height
    :param colour:colour - RGB
    :return:image
    """
    image = Image.new("RGB", (i, j), colour)
    return image


def get_pixel(image, x, y):
    """
    Return pixel from image about given coordinates x,y
    :param image:image
    :param i:x
    :param j:y
    :return:the value of pixel
    """
    width, height = image.size
    if x > width or y > height:
        return None
    pixel = image.getpixel((x, y))
    return pixel




def Roznica():
    root = Tk()
    root.withdraw()
    base1 = filedialog.askopenfilename(parent=root,initialdir="\\",
                                       title="Wybierz pierwszy obraz",
                                       filetypes=(("Image files", "*.jpg*"), ("all files", "*.*")))
    base1.replace('\\', '/')
    print(base1)
    image_1 = Image.open(base1)
    base2 = filedialog.askopenfilename(initialdir="\\",
                                       title="Wybierz drugi obraz",
                                       filetypes=(("Image files", "*.jpg*"), ("all files", "*.*")))
    base2.replace('\\', '/')
    image_2 = Image.open(base2)

    width1, height1 = image_1.size
    width2, height2 = image_2.size

    if width1 > width2:
        width = width1
    elif width1 == width2:
        width = width1
    else:
        width = width2

    if height1 > height2:
        height = height1
    elif height1 == height2:
        height = height1
    else:
        height = height2

    new_image = create_image(width, height, "black")
    pixels = new_image.load()
    width_1, height_1 = image_1.size
    width_2, height_2 = image_2.size

    for i in range(width):
        for j in range(height):

            if ((width_2<i+1<=width_1)and j+1<=height_1)or((height_2<j+1<=height_1)and i+1<=width_1):
                pixel = get_pixel(image_1, i, j)
                pixels[i, j] = (pixel[0], pixel[1],pixel[2])
            elif ((width_1<i+1<=width_2) and j+1<=height_2)or((height_1<j+1<=height_2)and i+1<=width_2):
                pixel2 = get_pixel(image_2, i, j)
                pixels[i, j] = (pixel2[0], pixel2[1],pixel2[2])
            elif (i+1>width_1 and j+1>height_2)or(i+1>width_2 and j+1>height_1) :
                pixels[i, j] = (0, 0, 0)
            else:
                pixel_1 = get_pixel(image_1, i, j)
                pixel_2 = get_pixel(image_2, i, j)
                pixels[i, j] = (difference(pixel_1[0],pixel_2[0]),difference(pixel_1[1],pixel_2[1]),difference(pixel_1[2],pixel_2[2]))

    return new_image


image3=Roznica()
image3.show()