import streamlit as st
from src.class_images import images_list


def choose_image(text="Choose image", k="basic"):
    choice = st.selectbox(text, options=images_list("images"), key=k)

    return choice


def run():
    st.title("Images")
    st.header("Show images")

    ch_im = choose_image()

    st.image(f"images/{ch_im}.jpeg", use_column_width=True)


if __name__ == "__main__":
    run()
