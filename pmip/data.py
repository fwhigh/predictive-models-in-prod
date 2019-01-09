import os
import pickle


def pickle_to_fs(obj=None, filename=None, subdirectory=None):
    if obj is None:
        raise ValueError("You must specify an obj")
    if filename is None:
        raise ValueError("You must specify a filename")
    if subdirectory is None:
        subdirectory = "."

    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    with open(os.path.join(subdirectory, filename), 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)


def load_from_fs_and_unpickle(filename=None, subdirectory=None):
    if filename is None:
        raise ValueError("You must specify a filename")
    if subdirectory is None:
        subdirectory = "."

    if not os.path.exists(subdirectory):
        raise ValueError('Directory {} does not exist'.format(subdirectory))

    with open(os.path.join(subdirectory, filename), 'rb') as pickle_file:
        obj = pickle.load(pickle_file)

    return obj


def download_glove():
    url = "http://www-nlp.stanford.edu/data/glove.840B.300d.zip"
