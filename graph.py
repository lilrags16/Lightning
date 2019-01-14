import numpy
import imageio
import scipy.misc
from datetime import datetime
from os import walk

f = []
ff = []
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    break
print f
for u in f:
    
    if u.split('.')[1] == 'mp4':
        ff.append(u)

for filename in ff:
    print filename
    start_time = datetime.now()
    vid = imageio.get_reader(filename,  'ffmpeg')
    num_frames = vid._meta['nframes']
    print 'Frames to do: ' + str(num_frames)
    values = []
    
    #f = open('values.txt', 'w')
    
    fps =  int(vid.get_meta_data()['fps'])
    
    array = numpy.zeros((int((num_frames/fps)),fps))
    print len(array)
    x = 0
    y = 0
    data = []
    mvavg = []
    mvavgg = []
    for num in range(1,num_frames-1):
        try:
            image = vid.get_data(num-1)
            Avg = (numpy.average(image))
            array[y-1][x] = Avg
            try:
                mvavgg.append(data[-1]/Avg)
            except:
                pass
            data.append(Avg)
            mvavg.append(numpy.average(data))
            
            x += 1
            if x == fps:
                
                y += 1
                x = 0
            f = (((1+x)*y)/num_frames)      
            #print 'Curent Second Counter: %s:%sf %s%%' % (y,x,f)    
        except:
            pass
    print 'Writing Files...'
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt 
      
    # x axis values 
    
    # corresponding y axis values 
    y = range(0,len(data))
    print len(data)
    print len(y)
    
    import statistics
    line = statistics.stdev(data)
    
    mvavgg_2 = [i * 20 for i in mvavgg]
    # plotting the points  
    plt.plot(y, data)
    plt.plot(y, mvavg,'r-')
    #print mvavgg
    plt.plot(range(0,len(mvavgg)), mvavgg_2,'g-')
    #plt.axhline(y=line, color='r', linestyle='-') 
    #plt.axhline(y=numpy.average(array), color='g', linestyle='-') 
    
      
    # naming the x axis 
    plt.xlabel('Frame') 
    # naming the y axis 
    plt.ylabel('Average Frame Value') 
    
    end_time = datetime.now()
    dur = 'Duration: %s' %(end_time - start_time)
      
    # giving a title to my graph 
    plt.title('%s: %s ' %(filename, dur)) 
      
    # function to show the plot 
    plt.savefig('graph_%s.png' % (filename.splt('.')[0]), dpi=200)
    
    '''
    print numpy.average(array)
    array_min = (array - 100)
    array_max = (array * (255.0/array.max()))
    array_avg = (array * (255.0/numpy.average(array)))
    
    scipy.misc.imsave('valmap_norm.png', array)
    scipy.misc.imsave('valmap_min.png', array_min)
    scipy.misc.imsave('valmap_max.png', array_max)
    scipy.misc.imsave('valmap_avg.png', array_avg)
    '''
