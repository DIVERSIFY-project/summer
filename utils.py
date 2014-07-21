# std libs
import logging
import json
import urllib2

# third-party

# our libs
import summerlogger

def get_relevant_streets(latitude, longitude, propagation_value=None):
    """
    This function is responsible for reverse-geocoding from a lat/long
    combination and creating a set of relevant_streets. By relevant streets, we     
    mean the way-id given in the OSM file.

    :param lattitude: The latitude of the sensor reading
    :type latitude: string
    :param longitude: The longitude of the sensor reading
    :type longitude: string
    :param propagation_value: The number of metres upto which the sensor's
    readings must be propagated
    :type sensor_name: string
    :returns: A set of all streets within propagation distance of the sensor, in 
    the form of openstreetmap's way-id
    """
    logger = logging.getLogger('summer.reverse_geocode.get_relevant_streets')
    prefix_url = \
    'http://services.gisgraphy.com/street/streetsearch?format=json'
    lat_url = '&lat='
    long_url = '&lng='

    full_url = ''.join([prefix_url,lat_url, str(latitude), long_url, str(longitude)])
    logger.debug("Connecting to: %s"%(full_url))
    geo_response = urllib2.urlopen(full_url)
    relevant_streets = set()
    if geo_response.code == 200:
        logger.debug("Received reverse geocoding information")
        json_geo = json.loads(geo_response.read())
        num_results = int(json_geo[u'numFound'])
        logger.info ("Number of results retrieved: %d"%(num_results,))
        all_streets = json_geo[u'result']
        for street in all_streets:
            street_distance = int(street[u'distance'])
            if street_distance > propagation_value:
                continue
            else:
                relevant_streets.add(street[u'openstreetmapId'])
    else:
        logger.warn("Could not retrieve reverse geocoding information")

    return relevant_streets


