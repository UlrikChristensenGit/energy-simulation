from pathlib import Path

from diskcache import Cache

CACHE_DIR = Path(__file__).parents[1] / ".diskcache"

cache = Cache(directory=CACHE_DIR)
