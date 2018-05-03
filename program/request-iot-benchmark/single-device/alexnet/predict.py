""" Run model prediction. """
from model import alexnet
import numpy as np

import os

def main():

    if os.environ.get('NO_GPU','')=='YES':
       os.environ['CUDA_VISIBLE_DEVICE']=''

    """ Call model construction function and run model multiple times. """
    model = alexnet()
    test_x = np.random.rand(224, 224, 3)
    x=model.predict(np.array([test_x]))
    for _ in range(50):
        model.predict(np.array([test_x]))


if __name__ == '__main__':
    main()
