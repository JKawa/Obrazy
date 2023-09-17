

import streamlit as st
from main import choose_image
from src.class_images import class_image
    
ch_im=choose_image()

c=class_image(ch_im)

shown_im=c.image

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





    
st.image(shown_im)
