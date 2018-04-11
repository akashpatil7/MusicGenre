import os
import numpy as np
from common import load_track,GENRE_LOOKUP
import fnmatch
import matplotlib
matplotlib.use('Agg')
from keras.models import load_model
import argparse
DEFAULT_SHAPE=(647,128)


class GenreClassifier:
    def __init__(self,data_set_path,extension):
        ##
        self.data_set_path=data_set_path
        self.file_meta=file = open('meta.txt','w')
        self.output_file=open('output.txt','w')
        self.file_list=[]
        self.extension=extension

    def create_data_pickle(self):
        output=np.array([])
        id=1
        for root, dirnames, filenames in os.walk(self.data_set_path):
            for filename in fnmatch.filter(filenames, '*.'+self.extension):
                full_file_path=os.path.join(root, filename)
                print('Processing '+full_file_path)
                self.file_list.append(full_file_path)
                self.file_meta.write(str(id)+'|'+full_file_path+'\n')
                mel_output,_=load_track(full_file_path,DEFAULT_SHAPE)
                mel_output=np.expand_dims(mel_output, axis=0)
                if output.shape[0] == 0:
                    output=mel_output
                else:
                    output=np.vstack((output,mel_output))
        print(output.shape)
        return output

    def predict(self,data_x):
        model = load_model('model/weights.h5')
        output = model.predict(data_x)
        data_y = np.argmax(output, axis=1)
        print (data_y.shape)
        for i in range(0,len(data_y)):
            predicted_genre=GENRE_LOOKUP[data_y[i]]
            self.output_file.write(str(i)+'|'+self.file_list[i]+'|'+predicted_genre+'\n')
        return data_y


def main():
    parser = argparse.ArgumentParser(description='Recognize the genre of music in a given folder')
    parser.add_argument('location',metavar='location',type=str,help='Folder location of the songs')
    parser.add_argument('extension',metavar='extension',type=str,help='Song extension like mp3',default='mp3')
    args=parser.parse_args()
    genre_classifier=GenreClassifier(args.location,args.extension)#'../genre-recognition-master/data/genres/hiphop'
    data_x=genre_classifier.create_data_pickle()
    genre_classifier.predict(data_x)


if __name__ == "__main__":
    main()
