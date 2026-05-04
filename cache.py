cache = {}

def get_from_cache(key):
    return cache.get(key)


def set_cache(key, value):
    cache[key] = value