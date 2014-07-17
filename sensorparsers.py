# std libs
import json
import urllib2
import xml.etree.ElementTree as ET

# third-party libs

# our libs
import constants
import summerlogger
import utils

def create_noise_sensor_hash():
    """
    This function reads an XML file created by NoiseTube, finds the appropriate
    streets that the readings pertain to, and creates a hash that can be
    inserted inside Redis. It ignores measurements that have no location 
    associated with them. If the same lat/long combination have multiple 
    measurements, the last one is taken

    :returns: Hash containing Way-id and sensor value and timestamp
    """
    logger = logging.getLogger('summer.reverse_geocode.create_noise_sensor_hash')
    SENSOR = 'NOISETUBE'
    logger.info("Parsing sensor data for: %s"%(SENSOR,))
    sensor_file = constants.getSensorSource(SENSOR)
    logger.debug("Sensor data being grabbed from:%s"%(sensor_file))
    sensor_hash = collections.defaultdict(int)
    for event, elem in ET.iterparse(sensor_file):
        if elem.tag == "measurement":
            loudness = elem.get('loudness')
            timestamp = elem.get('timeStamp')
            geoloc = elem.get('location')
            if geoloc is None:
                continue
            lat,long = geoloc.lstrip("geo:").split(",")
            relevant_streets = utils.get_relevant_streets(lat, long, SENSOR)
            for street in relevant_streets:
                sensor_hash[street] = {"value":loudness, "timestamp": 
                        timestamp}
    logger.info("Number of streets affected by sensor update: 
            %d"%(len(sensor_hash))
    return sensor_hash


