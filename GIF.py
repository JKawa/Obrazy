from PIL import Image
import imageio
import os
import imageio.v3
from tkinter import filedialog, Tk
from pathlib import Path
import glob


def create_image(i, j, color):
    image = Image.new("RGB", (i, j), color)
    return image

def difference(value1, value2):
    "Compute difference between two pixels value"
    a = abs(value1 - value2)
    if a > 255:
        a = a - 255
    else:
        pass
    return int(a)

def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:
        return None
    pixel = image.getpixel((i, j))
    return pixel



def Roznica(image_1, image_2):

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

def fill_picture(base_image, new_image):
    width_b, height_b = base_image.size
    width_n, height_n = new_image.size
    print(f"width b {width_b}, hight b {height_b}")
    print(f"width n {width_n}, hight n {height_n}")
    image_0 = create_image(width_b, height_b,'black')
    pixels_0 = image_0.load()
    for i in range(width_n):
        for j in range(height_n):
            if (i >= width_b or j >= height_b):
                pass
            else:
                if (i > width_n or j > height_n):
                    return None
                else:
                    pixel_n = get_pixel(new_image, i, j)
                    pixels_0[i, j] = (pixel_n[0], pixel_n[1], pixel_n[2])
    return image_0

def roznica_obraz(image_begin, image_end, step):
    """

    :param image_begin: obrazek początkowy od którego odejmujemy
    :param image_end: obrazek który odejmujemy
    :param step: ilość przejść
    :return:
    """
    (width, height) = image_begin.size
    image_rozn = create_image(width, height, "black")
    pixels_rozn = image_rozn.load()
    print(pixels_rozn)
    for i in range(width):
        for j in range(height):
            pixel_begin = get_pixel(image_begin, i, j)
            pixel_end = get_pixel(image_end, i, j)
            pixels_rozn[i, j] = (int(round(((((pixel_end[0]-pixel_begin[0])) / step)), 0)),
                                 int(round(((((pixel_end[1]-pixel_begin[1])) / step)), 0)),
                                 int(round(((((pixel_end[2]-pixel_begin[2])) / step)), 0)))
    return pixels_rozn

def zapis_giff(folder,wynik):
    images = list()
    for file in Path(folder).iterdir():

        if not file.is_file():
            continue
        images.append(imageio.v3.imread(file))

    for file in Path(folder).iterdir():
        head_tail = os.path.split(file)
        t=head_tail[1]
        print(t)
        r=t[7:].split(".")
        p=int(r[0])
        print(p)

        if not file.is_file():
            continue
        images[p-1]=(imageio.v3.imread(file))


    imageio.mimsave(f"{wynik}/giff.gif", images, duration = 0.2)

def pictures_to_giff():
    root = Tk()
    root.withdraw()
    base1 = filedialog.askopenfilename(parent=root,initialdir="\\",
        title="Wybierz pierwszy obraz",filetypes=(("Image files","*.jpg*"),("all files","*.*")))
    base1.replace('\\', '/')
    image_1=Image.open(base1)
    base2 = filedialog.askopenfilename(initialdir="\\",
        title="Wybierz drugi obraz",filetypes=(("Image files","*.jpg*"),("all files","*.*")))
    base2.replace('\\', '/')
    image_2 = Image.open(base2)
    print("Wybierz folder w którym zostaną umieszczone obrazy")
    folder = filedialog.askdirectory(title="Wybierz folder w którym zostaną umieszczone obrazy")
    folder.replace('\\', '/')
    print("Wybierz folder w którym zostanie umieszczony wynikowy gif")
    wynik = filedialog.askdirectory(title="Wybierz folder w którym zostanie umieszczony wynikowy gif")
    wynik.replace('\\', '/')
    step=int(input("Podaj ilość kroków"))

    roznica = Roznica(image_1, image_2)
    width_R, height_R = roznica.size
    print(f"width R {width_R}, height R:{height_R}")
    width_1, height_1 = image_1.size
    width_2, height_2 = image_2.size
    image_b = fill_picture(roznica, image_1)
    image_f = fill_picture(roznica, image_2)

    krok = 1
    while krok <= (step+1):

        print("krok: " ,krok)
        image_p=image_b
        image_p.save(folder+"/obrazek" + str(krok) + '.jpg', 'JPEG')
        pixels_p = image_p.load()
        for i in range(width_R):
            for j in range(height_R):
                #pixel_r = get_pixel(image_r, i, j)
                pixel_b = get_pixel(image_b, i, j)
                pixel_f = get_pixel(image_f, i, j)
                pixel_p=get_pixel(image_p, i, j)
                pixels_p[i, j] = (int(round((pixel_p[0] + (((pixel_f[0]-pixel_b[0]))/step)),0)),
                                  int(round((pixel_p[1] + (((pixel_f[1]-pixel_b[1]))/step)),0)),
                                  int(round((pixel_p[2] + (((pixel_f[2]-pixel_b[2]))/step)),0)))
        krok += 1
    zapis_giff(folder,wynik)
    print("Giff gotowy, zapisany we wskazanej lokalizacji")
    return

pictures_to_giff()




