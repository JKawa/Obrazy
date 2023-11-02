import streamlit as st
from main import choose_image
from src.class_images import class_image
import imageio
import os
import imageio.v3
from pathlib import Path
import base64
import numpy as np
import cv2 as cv

base = choose_image("Choose base image", "base")
B = class_image(base)


st.image(f"images/{base}.jpeg", use_column_width=True)
final = choose_image("Choose final image", "final")


F = class_image(final)

st.image(f"images/{final}.jpeg", use_column_width=True)

step = st.number_input("Choose number of steps", min_value=1)


def create_image(height, width):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    return image


def difference_pixel(value1, value2):
    "Compute difference between two pixels value"
    a = abs(value1 - value2)
    if a > 255:
        a = a - 255
    return int(a)


def get_pixel(img, i, j):
    height, width = img.shape[0], img.shape[1]
    if i > height or j > width:
        return None
    else:
        pixel = img[i, j]
        return pixel


def image_difference(image_1, image_2):
    height1, width1, _ = image_1.shape
    height2, width2, _ = image_2.shape

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

    new_image = np.zeros((height, width, 3), dtype=np.uint8)

    pixels = new_image
    height_1, width_1, _ = image_1.shape
    height_2, width_2, _ = image_2.shape

    for i in range(height):
        for j in range(width):
            if ((height_2 < i + 1 <= height_1) and j + 1 <= width_1) or (
                (width_2 < j + 1 <= width_1) and i + 1 <= height_1
            ):
                pixel = get_pixel(image_1, i, j)
                pixels[i, j] = (pixel[0], pixel[1], pixel[2])
            elif ((height_1 < i + 1 <= height_2) and j + 1 <= width_2) or (
                (width_1 < j + 1 <= width_2) and i + 1 <= height_2
            ):
                pixel2 = get_pixel(image_2, i, j)
                pixels[i, j] = (pixel2[0], pixel2[1], pixel2[2])
            elif (i + 1 > height_1 and j + 1 > width_2) or (
                i + 1 > height_2 and j + 1 > width_1
            ):
                pixels[i, j] = (0, 0, 0)
            else:
                pixel_1 = get_pixel(image_1, i, j)
                pixel_2 = get_pixel(image_2, i, j)
                pixels[i, j] = (
                    difference_pixel(pixel_1[0], pixel_2[0]),
                    difference_pixel(pixel_1[1], pixel_2[1]),
                    difference_pixel(pixel_1[2], pixel_2[2]),
                )

    return new_image


def fill_picture(base_image, new_image):
    height_b, width_b, _ = base_image.shape
    height_n, width_n, _ = new_image.shape
    image_0 = create_image(height_b, width_b)
    print("-----------------------------",get_pixel(image_0,1,1))
    pixels_0 = image_0
    for i in range(height_n):
        for j in range(width_n):
            if i >= height_b or j >= width_b:
                pass
            else:
                if i > height_n or j > width_n:
                    return None
                else:
                    pixel_n = get_pixel(new_image, i, j)
                    pixels_0[i, j] = (pixel_n[0], pixel_n[1], pixel_n[2])
    return image_0


def save_giff(folder, result):
    images = list()
    for file in Path(folder).iterdir():
        if not file.is_file():
            continue
        images.append(imageio.v3.imread(file))

    for file in Path(folder).iterdir():
        head_tail = os.path.split(file)
        t = head_tail[1]
        r = t[7:].split(".")
        p = int(r[0])

        if not file.is_file():
            continue
        images[p - 1] = imageio.v3.imread(file)

    imageio.mimsave(f"{result}/giff.gif", images, duration=0.2)


if st.button("create gif"):
    image_1 = B.image
    image_2 = F.image

    roznica = image_difference(image_1, image_2)
    height_R, width_R, _ = roznica.shape

    width_1, height_1 = B.width, B.height
    width_2, height_2 = F.width, F.height
    image_b = fill_picture(roznica, image_1)
    image_f = fill_picture(roznica, image_2)

    folder = "giff_images"
    result = "giff"

    stp = 1
    while stp <= (step + 1):
        image_p = image_b
        cv.imwrite(f"{folder}/obrazek{str(stp)}.jpg", image_p)
        pixels_p = image_p
        for i in range(height_R):
            for j in range(width_R):
                pixel_b = get_pixel(image_b, i, j)
                pixel_f = get_pixel(image_f, i, j)
                pixel_p = get_pixel(image_p, i, j)
                pixels_p[i, j] = (
                    int(round((pixel_p[0] + (((pixel_f[0] - pixel_b[0])) / step)), 0)),
                    int(round((pixel_p[1] + (((pixel_f[1] - pixel_b[1])) / step)), 0)),
                    int(round((pixel_p[2] + (((pixel_f[2] - pixel_b[2])) / step)), 0)),
                )
        stp += 1
    save_giff(folder, result)
    st.success("Giff gotowy, zapisany we wskazanej lokalizacji")

if st.button("show gif"):
    file_ = open(f"giff/giff.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
