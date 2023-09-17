import streamlit as st
from src.class_images import class_image
import pathlib
import os


def choose_image():
    for _, _, filenames in os.walk("images"):
        images_list=[f.split(".")[0] for f in filenames]
            
    choice=st.selectbox("Choose image to print",options=images_list)

    return choice



def run():
    st.title("Images")
    st.header("Show images")
    
    ch_im=choose_image()

    c=class_image(ch_im)
    
    st.image(c.image)














if __name__ == "__main__":
    run()