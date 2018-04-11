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

