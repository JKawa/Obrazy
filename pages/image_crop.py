import streamlit as st
from main import choose_image
from src.class_images import class_image
import cv2 as cv
import os

ch_im=choose_image()

c=class_image(ch_im)


st.sidebar.header("Choose process")


st.sidebar.subheader("Crop")


n=st.sidebar.number_input("Choose number of elements",min_value=0)
crop_button=st.sidebar.button("Crop")
if crop_button:
    for filename in os.listdir('Obrazy/saved_patches'):
        if os.path.isfile(os.path.join('Obrazy/saved_patches/', filename)):
            os.remove(os.path.join('Obrazy/saved_patches/', filename))

    W=c.width/n
    H=c.height/n
    for x in range(1,n+1):
        for y in range(1,n+1):
            if x==n and y==n:
                result=c.image_crop(int((x-1)*H),int(c.height)-1,int((y-1)*W),int(c.width)-1)
            elif x==n :
                result=c.image_crop(int((x-1)*H),int(c.height)-1,int((y-1)*W),int(y*W))
            elif y==n :
                result=c.image_crop(int((x-1)*H),int((x)*H),int((y-1)*W),int(c.width)-1)

            else:
                result=c.image_crop(int((x-1)*H),int((x)*H),int((y-1)*W),int(y*W))
            file_path = 'Obrazy/saved_patches/' + 'tile' + str(x) + '_' + str(y) + '.jpg'
            cv.imwrite(file_path, result)

    
    image_dir = "Obrazy/saved_patches"
    filenames = sorted(os.listdir(image_dir))
    
    fields = [f.split(".")[0] for f in filenames]
    fields = sorted(fields)

    num_images = len(fields)
    columns = n

    for idx in range(0, num_images, columns):
        cols = st.columns(columns)

        for i in range(columns):
            if idx + i < num_images:
                image_name = fields[idx + i]
                image_path = os.path.join(image_dir, image_name + ".jpg")
                cols[i].image(image_path, use_column_width=True)