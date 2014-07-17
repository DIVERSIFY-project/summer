"""
This contains all the constants needed for all the data gathering from
sensors, reading and writing from Redis, logging, etc.
"""

REDIS_CONSTANTS = {
    'REDIS_URL' = 'localhost',
    'HASH_NAME' = 'sensor_data',
    'KEY' = 'dublin_ways'
}

def getRedisConstants(constant):
    return REDIS_CONSTANTS.get(constant, False)

# Defines (in metres) how far the reading for this sensor should be propagated
SENSOR_PROPAGATION = {
        'NOISETUBE' = 50
}

def getSensorPropagation(constant):
    """
    Each sensor has a propagation strength. This is used to indicate how many 
    streets are affected by the sensor's readings. Greater the propagation 
    strength, greater the number of streets affected. If the sensor named in the 
    argument does not exist, a default value of 100 metres is returned.
    """
    return SENSOR_PROPAGATION.get(constant, 100)

SENSOR_CONSTANTS = {
        'NOISETUBE' = '/home/vivek/git/summer/sensor_readings/noise'
}
def getSensorNames():
    """
    Returns all sensors available. Essentially all the keys of SENSOR_CONSTANTS
    """
    return SENSOR_CONSTANTS.keys()

def getSensorSource(constant):
    """
    Returns the directory where all the sensor readings are stored

    :param constant: The sensor name
    :type constant: string
    :returns: string. The directory where all sensor readings are stored. If 
    sensor name is not found, returns False.
    """
    return SENSOR_CONSTANTS.get(constant, False)

SENSOR_PARSERS = {
        'NOISETUBE' : 'create_noise_sensor_hash'
        }
def getSensorParser(constant):
    """
    Returns the name of the function that can parse that particular sensor
    data. Every sensor might dump data in a different format, and might need a
    different parser. Also, we won't know which sensors are available for a
    particular city. Hence, we have to get the name of the parser function
    dynamically. 

    :param constant: Name of the sensor
    :type constant: string
    :returns: string. False, if constant not found
    """
    return SENSOR_PARSERS.get(constant, False)


LOGGING_CONSTANTS = {
        'LOGFILE' = '/tmp/summer.log',
        'MAX_LOG_SIZE' = 1048576, # 1 MEG
        'BACKUP_COUNT' = 5
}
def getLoggingConstants(constant):
    """
    Returns various constants needing by the logging module
    """
    return LOGGING_CONSTANTS.get(constant, False)
