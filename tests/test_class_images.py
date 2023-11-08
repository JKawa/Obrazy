import pytest
import numpy
from src.class_images import images_list, class_image


def test_basic():
    assert True


def test_image_list():
    actual = images_list("/home/caffee/kodzenie/repos/Images/Obrazy/images")
    assert isinstance(actual, list)


@pytest.fixture
def image():
    return class_image("kot")


def test_load_image(image):
    actual = image.load_image("kot")
    assert isinstance(actual, numpy.ndarray)


def test_resize(image):
    actual = image.resize(2)
    assert actual.shape[0] == image.height * 2 and actual.shape[1] == image.width * 2


def test_rotate(image):
    actual = image.rotate(50)
    assert isinstance(actual, numpy.ndarray)


def test_gray(image):
    actual = image.gray()
    assert isinstance(actual, numpy.ndarray)


def test_face_detection(image):
    actual = image.face_detection()
    assert isinstance(actual, str)


def test_image_crop(image):
    actual = image.image_crop(0, 5, 0, 5)
    assert isinstance(actual, numpy.ndarray)


def test_crop_n_parts(image):
    actual = image.crop_n_parts(2)
    assert isinstance(actual, list)
    assert len(actual) == 4
