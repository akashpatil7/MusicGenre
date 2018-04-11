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
