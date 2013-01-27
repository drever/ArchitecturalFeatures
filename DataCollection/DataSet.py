from PIL import Image
import numpy
import os
import definitions
import pickle

class DataSet:
    """Class initializer. All files in the image directory must have the same dimensions. Images are loaded and transformed into a numpy array for further analysis."""
    def __init__(self, image_directory_name):
        file_names = os.listdir(image_directory_name + definitions.subfolder_normalized)
        im = Image.open(image_directory_name + definitions.subfolder_normalized + file_names[0])
        self.imageSize = max(im.size[0], im.size[1])
        data_length = self.imageSize * self.imageSize
        number_of_files = len(file_names)
        self.imageData = numpy.zeros((number_of_files, self.imageSize * self.imageSize))

        for file_name, i in zip(file_names, range(number_of_files)):
            image = Image.open(image_directory_name + definitions.subfolder_normalized + file_name)
            a = numpy.array(image)
            s = image.size[0] * image.size[1]
            self.imageData[i, (data_length - s)/2:data_length - (data_length - s)/2] = a.reshape((1,  s))

        self.metaData = pickle.load(open(image_directory_name + definitions.meta_data_file_name, 'rb'))

        return

    def getImage(self, i):
        return Image.fromarray(self.imageData[i, :].reshape((self.imageSize, self.imageSize)))
    def getCoordinates(self, i):
        photo = self.metaData["photos"][i]
        return (photo["longitude"], photo["latitude"])