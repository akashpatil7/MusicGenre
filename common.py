# To avoid errors during importing librosa.
import matplotlib
matplotlib.use('Agg')

import numpy as np
import librosa as lbr
import keras.backend as K

GENRES = ['0', '1', '2', '3', '4', '5', '6','7']
GENRE_LOOKUP=['Hip-Hop','Pop','Folk/Blues/Country','Jazz','Rock/Metal','International/Reggae','Electronic','Instrumental']
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
