""" Run model prediction. """
from model import alexnet
import numpy as np
import tensorflow as tf
import keras

def main():

    import json
    import os
    import time
    timers={}

    STAT_REPEAT=os.environ.get('STAT_REPEAT','')
    if STAT_REPEAT=='' or STAT_REPEAT==None:
       STAT_REPEAT=50
    STAT_REPEAT=int(STAT_REPEAT)

    config = tf.ConfigProto()
#    config.gpu_options.allow_growth = True
#    config.gpu_options.allocator_type = 'BFC'
    config.gpu_options.per_process_gpu_memory_fraction = float(os.getenv('CK_TF_GPU_MEMORY_PERCENT', 33)) / 100.0

    sess = tf.Session(config=config) 
    keras.backend.set_session(sess)

    """ Call model construction function and run model multiple times. """
    model = alexnet()
    test_x = np.random.rand(224, 224, 3)
    x=model.predict(np.array([test_x]))

    dt=time.time()
    for _ in range(STAT_REPEAT):
        x=model.predict(np.array([test_x]))
        print (x)

    t=(time.time()-dt)/STAT_REPEAT

    timers['execution_time_classify']=t
    timers['execution_time']=t

    with open ('tmp-ck-timer.json', 'w') as ftimers:
         json.dump(timers, ftimers, indent=2)

if __name__ == '__main__':
    main()
