import pytest
import numpy
from pages.Create_gif import (
    create_image,
    difference_pixel,
    get_pixel,
    image_difference,
    fill_picture,
    save_giff,
)


def test_basic():
    assert True


def test_create_image():
    actual = create_image(10, 10)
    assert isinstance(actual, numpy.ndarray)
    assert actual.shape[0] == 10 and actual.shape[1] == 10


def test_difference_pixel():
    actual = difference_pixel(100, 50)
    assert actual == 50


def test_get_pixel():
    img = create_image(5, 5)
    actual = get_pixel(img, 1, 1)
    assert isinstance(actual, numpy.ndarray)
    assert actual[0] == 0


def test_image_difference():
    image1 = create_image(10, 10)
    image2 = create_image(10, 10)
    actual = image_difference(image1, image2)
    assert isinstance(actual, numpy.ndarray)
