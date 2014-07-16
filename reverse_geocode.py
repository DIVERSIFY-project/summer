# stdlib imports
import collections
import json
import urllib2
import xml.etree.ElementTree as ET

# third-party imports
import redis

# our code imports
import constants
import summerlogger



curr_lat = 53.34376885732333
curr_long = -6.240988668839767


def get_relevant_streets(latitude, longitude, sensor_name=None):
    """
    This function is responsible for reverse-geocoding from a lat/long
    combination and creating a set of relevant_streets. By relevant streets, we     
    mean the way-id given in the OSM file.

    :param lattitude: The latitude of the sensor reading
    :type latitude: string
    :param longitude: The longitude of the sensor reading
    :type longitude: string
    :param sensor_name: The name by which the sensor is identified. E.g., 
    'NOISETUBE'
    :type sensor_name: string
    :returns: A set of all streets within propagation distance of the sensor, in 
    the form of openstreetmap's way-id
    """
    logger = logging.getLogger('summer.reverse_geocode.get_relevant_streets')
    prefix_url = 
    'http://services.gisgraphy.com/street/streetsearch?format=json'
    lat_url = '&lat='
    long_url = '&lng='

    full_url = ''.join([prefix_url,lat_url, str(latitude), lng_url, 
        str(longitude)])
    geo_response = urllib2.urlopen(full_url)
    relevant_streets = set()
    if geo_response.code == 200:
        logger.debug("Received reverse geocoding information")
        json_geo = json.loads(geo_response.read())
        num_results = int(json_geo[u'numFound'])
        logger.info ("Number of results retrieved: %d"%(num_results,))
        all_streets = json_geo[u'result']
        sensor_propagation = constants.getSensorPropagation(sensor_name)
        for street in all_streets:
            street_distance = int(street[u'distance'])
            if street_distance > sensor_propagation:
                continue
            else:
                relevant_streets.add(street[u'openstreetmapId'])
    else:
        logger.warn("Could not retrieve reverse geocoding information")

    return relevant_streets

def create_noise_sensor_hash(sensor_file):
    """
    This function reads an XML file created by NoiseTube, finds the appropriate
    streets that the readings pertain to, and creates a hash that can be
    inserted inside Redis. It ignores measurements that have no location 
    associated with them. If the same lat/long combination have multiple 
    measurements, the last one is taken

    :param sensor_file: Absolute path to the XML file containing sensor data
    :type sensor_file: string
    :returns: Hash containing Way-id and sensor value
    """
    logger = logging.getLogger('summer.reverse_geocode.create_noise_sensor_hash')
    sensor_hash = collections.defaultdict(int)
    for event, elem in ET.iterparse(sensor_file):
        if elem.tag == "measurement":
            loudness = elem.get('loudness')
            timestamp = elem.get('timeStamp')
            geoloc = elem.get('location')
            if geoloc is None:
                continue
            lat,long = geoloc.lstrip("geo:").split(",")
            relevant_streets = get_relevant_streets(lat, long, 'NOISETUBE')
            for street in relevant_streets:
                sensor_hash[street] = loudness
    logger.info("Number of streets affected by sensor update: 
            %d"%(len(sensor_hash))
    return sensor_hash

def update_streets_with_sensor_data():
    """
    This method opens a connection to Redis, and for each sensor available
    updates street information with the sensor data that is read. Existing data
    about that street is overwritten.

    """
    logger = 
    logging.getLogger('summer.reverse_geocode.create_noise_sensor_hash')
    try:
        redis_url = constants.getRedisConstants('REDIS_URL')
        logger.debug("Connecting to Redis at: %s"%(redis_url,))
        redis_server = redis.Redis(redis_url)
        if not redis_server:
            logger.warn("Could not connect to Redis. Is it running?")
            raise IOError
     else:
        all_sensors = constants.getSensorNames()
        for sensor in all_sensors:
            # Get currently held data from redis

            # Get the source of sensor data
            # Read the source to get all data
            # For each datum, check if currently held data is more recent
            # if not, update value in sensor_hash
        



    
        


