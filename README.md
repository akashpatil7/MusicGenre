# MusicGenre

For installation of all the Python packages necessary:

*pip install -r requirements.txt*

You can train your own model by modifying and running model_training.py. Before that, Put your dataset into the /dataset directory and run datapickle.py. As a result, a .pkl file will be genreated which is then given as input to model_training.py.
On running model_training.py for that dataset, a HDF5 file will be generated in model folder. Give this file as input to run.py to classify the songs in the data/genres folder.

*python run.y data/genres mp3*

This classifier predicts the genre of the songs stored /data directory and outputs a output.txt file containing the genre of the song. Run initUI.py and select the song to be predicted from /data folder click on 'play' button.
