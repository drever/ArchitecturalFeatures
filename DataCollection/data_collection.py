import httplib
import json

import urllib

import os
import pickle

from PIL import Image
from PIL import ImageOps

import numpy

import pdb

import definitions

def main():
    image_list = query_image_list()
    image_directory_name = query_images_and_save(image_list, "test")
    normalize_images(image_directory_name)

def query_image_list(tag=None, size='medium', setp='public', rangep=(0, 1), region=((-180, -90), (180, 90)), mapFilter=False):
    query = "/map/get_panoramas.php?set=" + setp
    query += "&from=" + str(rangep[0]) + "&to=" + str(rangep[1])
    query += "&minx=" + str(region[0][0]) + "&miny=" + str(region[0][1]) + "&maxx" + str(region[1][0]) + "&maxy=" + str(region[1][1])
    query += "&size=" + size
    query += "&mapfilter=" + str(mapFilter)
    if tag != None:
        query += "&tag=" + tag

    print "Sending query " + query
    connection = httplib.HTTPConnection(definitions.image_server_url)
    connection.request("GET", query)
    response = connection.getresponse()
    data = response.read()
    jdata = json.loads(data)
    print "Recieved list with " + str(len(jdata["photos"])) + " image(s)."
    return jdata

def query_images_and_save(image_list, list_name):
    ldd = definitions.data_directory + list_name + "/"
    if not os.path.exists(ldd):
        os.makedirs(ldd)
    if not os.path.exists(ldd + definitions.subfolder_original):
        os.makedirs(ldd + definitions.subfolder_original)        
    pickle.dump(image_list, open(ldd + definitions.meta_data_file_name, "wb"))
    for photo in image_list["photos"]:
        print "loading from " + photo["photo_file_url"]
        file_name = ldd + definitions.subfolder_original + photo["photo_file_url"].split('/')[-1]
        print "saving to " + file_name        
        urllib.urlretrieve(photo["photo_file_url"], file_name)
    return ldd

def normalize_images(image_directory_name, image_size=100):
    ddn = image_directory_name + definitions.subfolder_normalized
    if not os.path.exists(ddn):
            os.makedirs(ddn)
    for image_name in os.listdir(image_directory_name + definitions.subfolder_original):
        image = Image.open(image_directory_name + definitions.subfolder_original + image_name)
        image.thumbnail((image_size, image_size))
        image = ImageOps.grayscale(image)
        image.save(ddn + image_name)

if __name__ == "__main__":
    main()
