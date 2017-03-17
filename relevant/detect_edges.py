import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.cm as cm
import scipy.misc
from PIL import Image
import scipy.io
import os
import shutil

import caffe

PREFIX_DIR = './'
INDEXES_DIR = PREFIX_DIR + 'indexed/'
EDGES_DIR = PREFIX_DIR + 'edges/'

if os.path.exists(EDGES_DIR):
    shutil.rmtree(EDGES_DIR)
os.makedirs(EDGES_DIR)

caffe.set_mode_gpu()
caffe.set_device(0)

def save_outputs(net, input_dir, batch_size, output_dir):
    files = os.listdir(input_dir)
    files.sort()
    list_len = len(files)
    start = 0
    stop = min(start+batch_size, list_len)
    while(start<list_len):
        batch_files = files[start:stop]
        in_ = []
        for file_name in batch_files:
            im = Image.open(input_dir+file_name).convert('RGB')
            im = np.array(im, dtype=np.float32)
            im = im[:,:,::-1]
            im -= np.array((104.00698793,116.66876762,122.67891434))
            im = im.transpose((2,0,1))
            in_.append(im)
        print(len(in_))
        in_ = np.asarray(in_)
        net.blobs['data'].reshape(*in_.shape)
        print(in_.shape)
        out = net.forward_all(data=in_)
        print(out['sigmoid-fuse'].shape)
        for i, file_name in enumerate(batch_files):
            fuse = out['sigmoid-fuse'][i,0,:,:]
            img = np.copy(1-fuse)
            scipy.misc.imsave(output_dir+file_name, img)
        start = stop
        stop = min(start+batch_size, list_len)

model_root = '../../examples/hed/'
net = caffe.Net(model_root+'deploy.prototxt', model_root+'hed_pretrained_bsds.caffemodel', caffe.TEST)
batch_size = 16
save_outputs(net, INDEXES_DIR, batch_size, EDGES_DIR)
