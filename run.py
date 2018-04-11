import os
import numpy as np
import fnmatch
import matplotlib
matplotlib.use('Agg')
from keras.models import load_model
import argparse
DEFAULT_SHAPE = (647,128)
import librosa as lbr
import keras.backend as K

GENRES = ['0', '1', '2', '3', '4', '5', '6','7','8','9','10']
GENRE_LOOKUP = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal',
        'pop', 'reggae', 'rock']

WINDOW_SIZE = 2048
WINDOW_STRIDE = WINDOW_SIZE // 2
N_MELS = 128
MEL_KWARGS = {
    'n_fft': WINDOW_SIZE,
    'hop_length': WINDOW_STRIDE,
    'n_mels': N_MELS
}

def load_track(filename, enforce_shape=None):
    new_input, sample_rate = lbr.load(filename, mono=True)
    features = lbr.feature.melspectrogram(new_input, **MEL_KWARGS).T
    
    if enforce_shape is not None:
        if features.shape[0] < enforce_shape[0]:
            delta_shape = (enforce_shape[0] - features.shape[0],
                           enforce_shape[1])
            features = np.append(features, np.zeros(delta_shape), axis=0)
        elif features.shape[0] > enforce_shape[0]:
            offset = features.shape[0] - enforce_shape[0]
            features = features[offset :, :]

    features[features == 0] = 1e-6
    return (np.log(features), float(new_input.shape[0]) / sample_rate)

class GenreClassifier:
        def __init__(self,data_set_path,extension):
                self.data_set_path=data_set_path
                self.file_meta=file = open('meta.txt','w')
                self.output_file=open('output.txt','w')
                self.file_list=[]
                self.extension=extension
                
def main():
    parser = argparse.ArgumentParser(description='Recognize the genre of music in a given folder')
    parser.add_argument('location',metavar='location',type=str,help='Folder location of the songs')
    parser.add_argument('extension',metavar='extension',type=str,help='Song extension like mp3',default='mp3')
    args=parser.parse_args()
