import streamlit as st
import cv2 as cv
import numpy as np


st.header("Choose picture to add")
# File uploader
image = st.file_uploader("Choose image to add", type=["jpg", "png", "jpeg"])
image_name = st.text_input("Add name")


def save_image(image, name, path):
    with open(f"{path}/{name}.jpeg", "wb") as f:
        f.write(image)


def image_bytes_from_file(image, name):
    file_bytes = image.read()
    with open(f"images/{name}.jpeg", "wb") as f:
        f.write(file_bytes)
    return file_bytes


def image_from_bites(bytes):
    np_array = np.fromstring(bytes, np.uint8)
    image = cv.imdecode(np_array, cv.IMREAD_COLOR)
    return image


if st.button("Add picture"):
    if image is not None and image_name is not None:
        im_bytes = image_bytes_from_file(image, image_name)
        image = image_from_bites(im_bytes)
    else:
        st.error("")

    st.image(image, channels="BGR")
