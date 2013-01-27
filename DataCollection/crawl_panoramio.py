import httplib
import json

import urllib

import os
import pickle

from PIL import Image
from PIL import ImageOps

data_directory = "../Data/"
image_server_url = "www.panoramio.com"
subfolder_normalized = "normalized/"
subfolder_original = "original/"

def main():
    image_list = query_image_list()
    image_directory_name = query_images(image_list, "test")
    normalize_images(image_directory)

def query_image_list(tag=None, size='medium', setp='public', rangep=(0, 100), region=((-180, -90), (180, 90)), mapFilter=False):
    query = "/map/get_panoramas.php?set=" + setp
    query += "&from=" + str(rangep[0]) + "&to=" + str(rangep[1])
    query += "&minx=" + str(region[0][0]) + "&miny=" + str(region[0][1]) + "&maxx" + str(region[1][0]) + "&maxy=" + str(region[1][1])
    query += "&size=" + size
    query += "&mapfilter=" + str(mapFilter)
    if tag != None:
        query += "&tag=" + tag

    print "Sending query " + query
    connection = httplib.HTTPConnection(image_server_url)
    connection.request("GET", query)
    response = connection.getresponse()
    data = response.read()
    jdata = json.loads(data)
    print "Recieved list with " + str(len(jdata["photos"])) + " image(s)."
    return jdata

def query_images_and_save(image_list, list_name):
    ldd = data_directory + list_name + "/"
    if not os.path.exists(ldd):
        os.makedirs(ldd)
    pickle.dump(image_list, open(ldd + "metadata.p", "wb"))
    for photo in image_list["photos"]:
        print "loading from " + photo["photo_url"]
        file_name = ldd + subfolder_original + photo["photo_file_url"].split('/')[-1]
        urllib.urlretrieve(photo["photo_file_url"], file_name)
        print "saving to " + file_name
    return ldd

def normalize_images(image_directory_name, image_size=100):
    ddn = image_directory_name + subfolder_normalized
    if not os.path.exists(ddn):
            os.makedirs(ddn)
    for image_name in os.listdir(image_directory_name + subfolder_original):
        image = Image.open(image_directory_name + subfolder_original + image_name)
        ml = max(image.size)
        image = image.resize((ml / image.size[0] * image_size, ml / image.size[1] * image_size))
        image = ImageOps.grayscale(image)
        image.save(ddn + image_name)
if __name__ == "__main__":
    main()
