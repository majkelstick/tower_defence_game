import pygame as py
import os

def load_image(path, width, height):
    return py.transform.scale(py.image.load(path), (width, height))