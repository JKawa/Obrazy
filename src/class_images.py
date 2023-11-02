import cv2 as cv
import os


def images_list(dir):
    for _, _, filenames in os.walk(dir):
        images_list = [f.split(".")[0] for f in filenames]
    return images_list


class class_image:
    def __init__(self, name):
        self.image = self.load_image(name)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

    def load_image(self, name, path="images"):
        im = cv.imread(f"{path}/{name}.jpeg")
        return im

    def resize(self, scale):
        res = cv.resize(
            self.image,
            (scale * self.width, scale * self.height),
            interpolation=cv.INTER_CUBIC,
        )
        return res

    def rotate(self, angle):
        M = cv.getRotationMatrix2D(
            ((self.width - 1) / 2.0, (self.height - 1) / 2.0), int(angle), 1
        )
        dst = cv.warpAffine(self.image, M, (self.width, self.height))
        return dst

    def gray(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        return gray

    def face_detection(self):
        face_cascade = cv.CascadeClassifier("src/haarcascade_frontalface_default.xml")
        grayImage = self.gray()
        print(grayImage)
        faces = face_cascade.detectMultiScale(
            grayImage, scaleFactor=1.1, minNeighbors=5
        )
        print(type(faces))
        if len(faces) == 0:
            return "No faces found"

        else:
            print(faces)
            print(faces.shape)
            print("Number of faces detected: " + str(faces.shape[0]))

            for x, y, w, h in faces:
                cv.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 1)

            cv.rectangle(
                self.image,
                ((0, self.image.shape[0] - 25)),
                (270, self.image.shape[0]),
                (255, 255, 255),
                -1,
            )
            cv.putText(
                self.image,
                "Number of faces detected: " + str(faces.shape[0]),
                (0, self.image.shape[0] - 10),
                cv.FONT_HERSHEY_TRIPLEX,
                0.5,
                (0, 0, 0),
                1,
            )
            return str(faces.shape[0])

    def image_crop(self, start_row, end_row, start_col, end_col):
        cropped = self.image[start_row:end_row, start_col:end_col]
        return cropped

    def crop_n_parts(self, n):
        W = self.width / n
        H = self.height / n
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                if x == n and y == n:
                    result = self.image_crop(
                        int((x - 1) * H),
                        int(self.height) - 1,
                        int((y - 1) * W),
                        int(self.width) - 1,
                    )
                elif x == n:
                    result = self.image_crop(
                        int((x - 1) * H),
                        int(self.height) - 1,
                        int((y - 1) * W),
                        int(y * W),
                    )
                elif y == n:
                    result = self.image_crop(
                        int((x - 1) * H),
                        int((x) * H),
                        int((y - 1) * W),
                        int(self.width) - 1,
                    )
                else:
                    result = self.image_crop(
                        int((x - 1) * H), int((x) * H), int((y - 1) * W), int(y * W)
                    )
                cv.imwrite(
                    "saved_patches/" + "tile" + str(x) + "_" + str(y) + ".jpg", result
                )

        return sorted([f.split(".")[0] for f in sorted(os.listdir("saved_patches/"))])
