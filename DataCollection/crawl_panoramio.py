import httplib
import json

import urllib

import os
import pickle

data_directory = "../Data/"
image_server_url = "www.panoramio.com"

def main():
    image_list = query_image_list()
    query_images(image_list, "test")

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

def query_images(image_list, list_name):
    ldd = data_directory + list_name + "/"
    if not os.path.exists(ldd):
        os.makedirs(ldd)
    pickle.dump(image_list, open(ldd + "metadata.p", "wb"))
    for photo in image_list["photos"]:
        print "loading from " + photo["photo_url"]
        file_name = ldd + photo["photo_file_url"].split('/')[-1]
        urllib.urlretrieve(photo["photo_file_url"], file_name)
        print "saving to " + file_name

if __name__ == "__main__":
    main()
