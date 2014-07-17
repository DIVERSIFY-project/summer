# stdlib imports
import collections
import json
import urllib2
import xml.etree.ElementTree as ET

# third-party imports
import jsonpickle
import redis

# our code imports
import constants
import sensorparsers
import summerlogger



curr_lat = 53.34376885732333
curr_long = -6.240988668839767


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
        logger.info("Connected to Redis")
        # Get currently held data from redis
        HASH_NAME = constants.getRedisConstants('HASH_NAME')
        logger.debug("Getting hash called:%s"%(HASH_NAME))
        KEY = constants.getRedisConstants('KEY')
        city_sensor_data = redis_server.hget(HASH_NAME, KEY)
        city_sensor_hash = jsonpickle.decode(city_sensor_data)
        all_sensors = constants.getSensorNames()
        
        for sensor in all_sensors:
            sensor_parser = getattr(sensorparsers, sensor)
            new_sensor_data =  sensor_parser()
            

        



    
        


