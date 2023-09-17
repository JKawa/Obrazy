from PIL import Image, ImageFilter
import cv2 as cv

class class_image():
    def __init__(self,name):
        self.image=self.load_image(name)
        self.height=self.image.shape[0]
        self.width=self.image.shape[1]
        
        
    def load_image(self,name, path="images"):
        im = cv.imread(f'{path}/{name}.jpeg')
        return im
    def show_image(self):
        self.image.show()
        
    def resize(self,scale):
        res = cv.resize(self.image,(scale*self.width, scale*self.height), interpolation = cv.INTER_CUBIC)
        return res
    
    def rotate(self,angle):
        M = cv.getRotationMatrix2D(((self.width-1)/2.0,(self.height-1)/2.0),int(angle),1)
        dst = cv.warpAffine(self.image,M,(self.width,self.height))
        return dst
    def grey(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        return gray
    
    def face_detection(self):
        face_cascade = cv.CascadeClassifier('src/haarcascade_frontalface_default.xml')
        grayImage = self.grey()
        faces = face_cascade.detectMultiScale(grayImage)
        print (type(faces))
        if len(faces) == 0:
            return "No faces found"
  
        else:
            print (faces)
            print (faces.shape)
            print ("Number of faces detected: " + str(faces.shape[0]))
        
            for (x,y,w,h) in faces:
                cv.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),1)
        
            cv.rectangle(self.image, ((0,self.image.shape[0] -25)),(270, self.image.shape[0]), (255,255,255), -1)
            cv.putText(self.image, "Number of faces detected: " + str(faces.shape[0]), (0,self.image.shape[0] -10), cv.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
            return str(faces.shape[0])
        
        
        
c=class_image("kot")
print(type(c.image))
print(c.height)
print(c.width)

        
