"""
This contains all the constants needed for all the data gathering from
sensors, reading and writing from Redis, etc.
"""

REDIS_CONSTANTS = {
    'REDIS_URL' = 'localhost',
    'REDIS_HASHES' = 'sensors'
}

def getRedisConstants(constant):
    return REDIS_CONSTANTS.get(constant, False)

