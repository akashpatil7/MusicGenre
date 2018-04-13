'''
GPU command:
THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python model_training.py

device=gpu : When device is set to GPU computations become faster
floatX=float32 is to ensure that output variables have a float32 data type
'''
from keras.callbacks import Callback
from keras.utils import np_utils
from keras.models import Model
from keras.optimizers import RMSprop,Adam
from keras import backend as K
from keras.layers import Input, Dense, Lambda, Dropout, Activation, LSTM, \
        TimeDistributed, Convolution1D, MaxPooling1D,Conv1D,AveragePooling1D, Flatten,GlobalAveragePooling1D,GlobalMaxPooling1D,concatenate
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from optparse import OptionParser
from sys import stderr, argv
import os
import tensorflow as tf

GENRES = ['Hip-Hop','Pop','Folk/Country','Jazz','Rock/Metal','Reggae/Intl','Electronic','Instrumental']

SEED = 42
N_LAYERS = 3
FILTER_LENGTH = 5
CONV_FILTER_COUNT = 256
LSTM_COUNT = 256 #long short term memory networks
BATCH_SIZE = 32  #Total number of training examples present in a single batch.Dataset is divided into number of batches.
EPOCH_COUNT = 100 #Number of times the entire dataset is passed through the neural network.
# The number of batches is equal to number of iterations for one epoch.
def weightedCustom(x):
    weights=np.arange(77)
    weights=weights[:,np.newaxis]
    weightsKeras=K.variable(value=weights)
    values_tensor=x
    out=values_tensor*weights
    out=K.sum(out,axis=1)
    out=tf.divide(out,3003)#1+2+3+.....+77
    return out



def train_model(data):
'''
Split arrays or matrices into random train and test subsets where test_size = 0.2 or 20%
of the data set
'''     
    x = data['x']
    y = data['y']
    (x_train, x_val, y_train, y_val) = train_test_split(x, y,stratify=y, test_size=0.2,random_state=SEED)  

    print 'Building model...'

    input_shape = (x_train.shape[1], x_train.shape[2]) #required when using a layer as the first layer in a model.
    print input_shape
    model_input = Input(shape=input_shape)
    layer = model_input
    for i in range(3):
	'''
	 filters : the number of output filters in the convolution.
	 kernel_size : An integer specifying the length of the 1D convolution window.
	 Strides : An integer specifying the stride length of the convolution.
	 '''
        layer = Conv1D(filters=256, kernel_size=4,strides=2)(layer) 
        layer = Activation('relu')(layer)
        layer = MaxPooling1D(2)(layer)
    averagePool = GlobalAveragePooling1D()(layer)
    maxPool = GlobalMaxPooling1D()(layer)
    layer = concatenate([averagePool, maxPool])
    layer = Dropout(rate=0.5)(layer)
    layer = Dense(units=len(GENRES))(layer)
    model_output = Activation('softmax')(layer)
    model = Model(model_input, model_output)
    opt = Adam()
    model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])
    model.fit(x_train, y_train,batch_size=BATCH_SIZE,epochs=80,validation_data=(x_val, y_val),verbose=1)
    return model

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--data_path', dest='data_path',
            default=os.path.join(os.path.dirname(__file__),
                'data/data.pkl'),
            help='path to the data pickle', metavar='DATA_PATH')
    parser.add_option('-m', '--model_path', dest='model_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/model.yaml'),
            help='path to the output model YAML file', metavar='MODEL_PATH')   
    parser.add_option('-w', '--weights_path', dest='weights_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/weights.h5'),
            help='path to the output model weights hdf5 file',
            metavar='WEIGHTS_PATH')
    

    with open(options.data_path, 'rb') as f:
        data = pickle.load(f)

        model=train_model(data)

    with open(options.model_path, 'w') as f:
        f.write(model.to_yaml())
    model.save_weights(options.weights_path)

#model.save('models/weights.h5')

