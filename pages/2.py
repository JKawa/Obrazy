import streamlit as st
from main import choose_image
from src.class_images import class_image

ch_im=choose_image()

c=class_image(ch_im)

shown_im=c.image

st.sidebar.header("Choose process")


st.sidebar.subheader("Face recognition")

face_button=st.sidebar.button("Find faces")
if face_button:
    number_of_faces=c.face_detection()
    st.success(number_of_faces)
st.sidebar.markdown("---------------------------")














st.image(shown_im)
