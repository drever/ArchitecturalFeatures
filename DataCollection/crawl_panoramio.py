import httplib
import json

import urllib

data_directory = "../Data/"

def main():
    panoramio_response = query_panoramio()
    query_images(panoramio_response)

def query_panoramio(tag=None, size='medium', setp='public', rangep=(0, 1), region=((-180, -90), (180, 90)), mapFilter=False):
    query = "/map/get_panoramas.php?set=" + setp
    query += "&from=" + str(rangep[0]) + "&to=" + str(rangep[1])
    query += "&minx=" + str(region[0][0]) + "&miny=" + str(region[0][1]) + "&maxx" + str(region[1][0]) + "&maxy=" + str(region[1][1])
    query += "&size=" + size
    query += "&mapfilter=" + str(mapFilter)
    if tag != None:
        query += "&tag=" + tag

    print "Sending query " + query
    connection = httplib.HTTPConnection("www.panoramio.com")
    connection.request("GET", query)
    response = connection.getresponse()
    data = response.read()
    jdata = json.loads(data)
    return jdata

def query_images(panoramio_response):
    for photo in panoramio_response["photos"]:
        print "loading from" + photo["photo_url"]

        file_name = data_directory + photo["photo_file_url"].split('/')[-1]
        urllib.urlretrieve(photo["photo_file_url"], file_name)

        print "saving to " + file_name

if __name__ == "__main__":
    main()
