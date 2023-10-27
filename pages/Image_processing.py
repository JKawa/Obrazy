import os

import streamlit as st
from main import choose_image
from src.class_images import class_image
    
ch_im=choose_image()

c=class_image(ch_im)


def delete_files_from_dir(dir):
    for filename in os.listdir(dir):
        if os.path.isfile(os.path.join(f'{dir}/', filename)):
            os.remove(os.path.join(f'{dir}/', filename))
    return dir

st.sidebar.header("Choose process")

st.sidebar.subheader("Resize")
s,r=st.sidebar.columns(2)
resize_button=r.button("resize")
scale=s.number_input("Add scale", step=1, key="scale")
if resize_button:
    shown_im=c.resize(scale)
st.sidebar.markdown("---------------------------")

st.sidebar.subheader("Rotate")
s,r=st.sidebar.columns(2)
rotate_button=r.button("rotate")
angle=s.number_input("Add angle", step=1, key="angle")
if rotate_button:
    shown_im=c.rotate(angle)
st.sidebar.markdown("---------------------------")

st.sidebar.subheader("Grey scale")

grey_button=st.sidebar.button("Grey")
if grey_button:
    shown_im=c.grey()
st.sidebar.markdown("---------------------------")

st.image(f"images/{ch_im}.jpeg", use_column_width=True)

st.sidebar.subheader("Crop")


n=st.sidebar.number_input("Choose number of elements",min_value=0)
crop_button=st.sidebar.button("Crop")
if crop_button:
    delete_files_from_dir('saved_patches')

    fields=c.crop_n_parts(n)

    for idx in range(0, len(fields), n):
        cols = st.columns(n)

        for i in range(n):
            if idx + i < len(fields):
                image_name = fields[idx + i]
                image_path = os.path.join('saved_patches/', image_name + ".jpg")
                cols[i].image(image_path, use_column_width=True)

st.sidebar.markdown("---------------------------")

    

