from model import vgg16
import numpy as np

def main():

    import json
    import os
    import time
    timers={}

    STAT_REPEAT=os.environ.get('STAT_REPEAT','')
    if STAT_REPEAT=='' or STAT_REPEAT==None:
       STAT_REPEAT=50
    STAT_REPEAT=int(STAT_REPEAT)

    """ Call model construction function and run model multiple times. """
    model = vgg16()
    test_x = np.random.rand(224, 224, 3)

    dt=time.time()
    for _ in range(STAT_REPEAT):
        model.predict(np.array([test_x]))

    t=(time.time()-dt)/STAT_REPEAT

    timers['execution_time_classify']=t
    timers['execution_time']=t

    with open ('tmp-ck-timer.json', 'w') as ftimers:
         json.dump(timers, ftimers, indent=2)

if __name__ == '__main__':
    main()
