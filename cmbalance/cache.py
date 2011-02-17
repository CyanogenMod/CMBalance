from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache = CacheManager(**parse_cache_config_options({
            'cache.type': 'memory',
            'cache.lock_dir': '/tmp/cache/lock'
            }))
