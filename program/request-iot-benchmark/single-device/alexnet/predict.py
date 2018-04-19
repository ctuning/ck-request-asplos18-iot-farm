""" Run model prediction. """
from model import alexnet
import numpy as np

import sys

from keras.applications import vgg16

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

def main():
    """ Call model construction function and run model multiple times. """

    a=sys.argv

    image=a[1]

    original = load_img(image, target_size=(224, 224))
    numpy_image = img_to_array(original)
    image_batch = np.expand_dims(numpy_image, axis=0)

    alexnet_model = vgg16.VGG16(weights='imagenet')

    model = alexnet()
    test_x = np.random.rand(224, 224, 3)
    x=model.predict(np.array([test_x]))
    print (x)
    for _ in range(50):
        model.predict(np.array([test_x]))


if __name__ == '__main__':
    main()
