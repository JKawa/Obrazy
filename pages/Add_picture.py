import streamlit as st
import cv2 as cv
import numpy as np
import requests
import json


st.header("Choose picture to add")
st.subheader(
    "Choose an image to upload or write a word to upload the picture from wikiipedia"
)
# File uploader
image = st.file_uploader("Choose image to add", type=["jpg", "png", "jpeg"])
image_name = st.text_input("Add name")


def save_image(image, name, path="images"):
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


if st.button("Add picture", key="picture_upload"):
    if image is not None and image_name is not None:
        im_bytes = image_bytes_from_file(image, image_name)
        image = image_from_bites(im_bytes)
        st.image(
            image,
        )
    else:
        st.error("Please upload an image and write name")


st.subheader("Insert a word")

ch_image = st.text_input("Add word")


def get_wiki_image(title):
    url = "https://en.wikipedia.org/w/api.php"
    data = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "pageimages|pageterms",
        "piprop": "original",
        "titles": title,
    }
    response = requests.get(url, data)
    json_data = json.loads(response.text)
    return (
        json_data["query"]["pages"][0]["original"]["source"]
        if len(json_data["query"]["pages"]) > 0
        else "Not found"
    )


def get_image_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        image_bytes = np.frombuffer(response.content, np.uint8)
        image = cv.imdecode(image_bytes, cv.IMREAD_COLOR)
    return image


if st.button("Add picture", key="picture_wikipedia"):
    if ch_image != "":
        try:
            img_url = get_wiki_image(ch_image)
            st.markdown(img_url)
            st.image(img_url)
            img = get_image_from_url(img_url)
            save_path = f"images/{ch_image}.jpeg"
            cv.imwrite(save_path, img)
        except Exception:
            st.error("Please try again")
    else:
        st.error("Please insert word")
