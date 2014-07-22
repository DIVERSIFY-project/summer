# stdlib imports
import collections
import ConfigParser
import importlib
import json
import logging
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


def update_streets_with_sensor_data(city_config_file):
    """
    This method opens a connection to Redis, and for each sensor available
    updates street information with the sensor data that is read. Existing data
    about that street is overwritten.

    """
    logger = logging.getLogger('summer.reverse_geocode.create_noise_sensor_hash')
    try:
        config = ConfigParser.SafeConfigParser()
        config.read(city_config_file)

        redis_url = config.get('ConnectionSettings', 'REDIS_URL')
        logger.debug("Connecting to Redis at: %s"%(redis_url,))
        redis_server = redis.Redis(redis_url)
        if not redis_server:
            logger.warn("Could not connect to Redis. Is it running?")
            raise IOError
    except IOError as ioe:
        logger.critical("Cannot connect to datastore Redis: %s"%(ioe))
    else:
        logger.info("Connected to Redis")
        # Get currently held data from redis
        city_prefix = config.get('ConnectionSettings', 'CITY_PREFIX')
        city_way_set = ''.join([city_prefix, '_set'])
        city_way_data = redis_server.smembers(city_way_set)
        logger.debug("Number of items inside set %s is: %d"%(city_prefix, len(city_way_data)))

        all_sensors = config.options('SensorsAvailable')
        logger.info("Number of sensors available: %d"%(len(all_sensors)))
        
        for sensor in all_sensors:
            sensor_name = config.get('SensorsAvailable', sensor)
            logger.info("Starting with sensor %s"%(sensor_name))
            configvals = config.items(sensor_name)
            sensor_config = collections.defaultdict(str)
            for val in configvals:
                sensor_config[val[0]] = val[1]
            logger.debug(sensor_config)
            parser_module, parser_func = \
                sensor_config['parser'].split('.')
            parserlib = importlib.import_module(parser_module)
            sensor_parser = getattr(parserlib, parser_func)
            sensor_file = sensor_config['dirname'] + sensor_config['filename']
            sensor_propagation = float(sensor_config['propagation'])
            sensor_data = sensor_parser(sensor_name, sensor_file, sensor_propagation)
#            HASH_NAME = ''.join([city_prefix, '_hash'])
#            logger.debug("Getting hash called:%s"%(HASH_NAME))
#            redis_way_hash = collections.defaultdict(str)

            logger.debug(sensor_data)
            for street, street_data in sensor_data.items():
                logger.debug("Adding data for street: %s"%(street))
                city_way_data.add(street)
                redis_server.sadd(city_way_set, street)
                # Write the hash data back to Redis
                for key,value in street_data.items():
                    redis_server.hset(street, key,value)
                    logger.debug("Inserted hash: %s with %s=>%s"%(street, key, value))

            logger.info("Finished with sensor: %s"%(sensor_name))
        return True

       
if __name__ == '__main__':
    update_streets_with_sensor_data('/home/vivek/git/diversify-summer/dublin.config')
