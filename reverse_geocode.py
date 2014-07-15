# stdlib imports
import collections
import json
import urllib2
import xml.etree.ElementTree as ET

# third-party imports
import redis
import rq

# our code imports
import constants



curr_lat = 53.34376885732333
curr_long = -6.240988668839767

REDIS_URL = 'http://localhost'

def get_relevant_streets(latitude, longitude):
    """
    This function is responsible for reverse-geocoding from a lat/long
    combination and creating a set of relevant_streets. By relevant streets, we     
    mean the way-id given in the OSM file.
    """

    prefix_url = 
    'http://services.gisgraphy.com/street/streetsearch?format=json'
    lat_url = '&lat='
    long_url = '&lng='

    full_url = ''.join([prefix_url,lat_url, str(latitude), lng_url, 
        str(longitude)])
    geo_response = urllib2.urlopen(full_url)
    relevant_streets = set()
    if geo_response.code == 200:
        print("Received reverse geocoding information")
        json_geo = json.loads(geo_response.read())
        num_results = int(json_geo[u'numFound'])
        print ("Number of results retrieved: %d"%(num_results,))
        all_streets = json_geo[u'result']
        for street in all_streets:
            relevant_streets.add(street[u'openstreetmapId'])
    else:
        print("Could not retrieve reverse geocoding information")

    return relevant_streets

def create_noise_sensor_hash(sensor_file):
    """
    This function reads an XML file created by NoiseTube, finds the appropriate
    streets that the readings pertain to, and creates a hash that can be
    inserted inside Redis. It ignores measurements that have no location 
    associated with them. If the same lat/long combination have multiple 
    measurements, the last one is taken

    Args: Absolute path to the XML file containing sensor data
    Return: Hash containing Way-id and sensor value
    """
    sensor_hash = collections.defaultdict(int)
    for event, elem in ET.iterparse(sensor_file):
        if elem.tag == "measurement":
            loudness = elem.get('loudness')
            timestamp = elem.get('timeStamp')
            geoloc = elem.get('location')
            if geoloc is None:
                continue
            lat,long = geoloc.lstrip("geo:").split(",")
            relevant_streets = get_relevant_streets(lat, long)
            for street in relevant_streets:
                sensor_hash[street] = loudness

    return sensor_hash


    
        


