import pytest
import numpy
from pages.Add_picture import get_wiki_image, get_image_from_url

def test_basic():
    assert True
    
    
def test_get_wiki_image():
    actual=get_wiki_image("horse")
    assert isinstance(actual, str)
    
    
def test_get_image_from_url():
    actual=get_image_from_url("https://upload.wikimedia.org/wikipedia/commons/1/15/Cat_August_2010-4.jpg")
    assert isinstance(actual,numpy.ndarray)