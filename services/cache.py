import time

CACHE = {}
TTL = 300  # seconds


def get(key):
    item = CACHE.get(key)
    if not item:
        return None

    value, ts = item

    if time.time() - ts > TTL:
        CACHE.pop(key, None)
        return None

    return value


def set(key, value):
    CACHE[key] = (value, time.time())
