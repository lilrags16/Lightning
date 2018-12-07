import pylab
import imageio
import numpy as np
import scipy.misc
import time
from datetime import datetime

def lightningExport(sq,filename):
    start_time = datetime.now()
    vid = imageio.get_reader(filename,  'ffmpeg')
    num_frames=vid._meta['nframes']
    print 'Frames to do: ' + str(num_frames)
    values = []
    dome = 1
    wait = 0
    f = open('values.txt', 'w')
    
    fps =  int(vid.get_meta_data()['fps'])
    for num in range(1,num_frames-1):
        lap_start = datetime.now()
        image1 = vid.get_data(num-1)
        image2 = vid.get_data(num)
        
        
        Avg1 = (np.average(image1)-sq)
        Avg2 = (np.average(image2)-sq)
        
        values.append(Avg2)
        print "Frame " + str(num) + ' of ' + str(num_frames)
        value = abs((Avg2-Avg1)*100)
        f.write(str(value)+'\n')
        f.flush()
        if wait == 0:
            if dome == 1:
                if (value >= 100):
                    for frame in range(-fps,fps):
                        scipy.misc.imsave('strike_'+str(num)+'_'+ str(frame) +'_.jpg', vid.get_data(num+frame))
                        print "FRAME SAVED"
                        wait = fps
        if wait != 0:
            wait = wait-1
        lap_end = datetime.now()
        print 'Time Remaining: {}'.format(abs(lap_start - lap_end)*(num_frames-num))
        print 'Time Per Frame: {}'.format(abs(lap_start - lap_end)) + '\n'
        
    for i in values:
        print i
    
    # do your work here
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

#lightningExport(100,110)
