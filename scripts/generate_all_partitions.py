import datetime
import json
import logging

from upstash_redis import Redis

from blokk_solver.combinatorics import generate_cube_volume_samples

logger = logging.getLogger(__name__)

redis = Redis.from_env()
redis.set("last_touched", datetime.datetime.now(datetime.UTC).isoformat())


now = datetime.datetime.now(datetime.UTC).isoformat()
redis.set(
    "n=27",
    json.dumps({"last_touched": now}),
)


blokk_partitions = generate_cube_volume_samples(cube_volume=27)

logger.debug(blokk_partitions)

pipeline = redis.pipeline()

pipeline.set("foo", 1)
pipeline.incr("foo")
pipeline.get("foo")

n = 27
for p in blokk_partitions:
    p_hash = hash_partition(n, p)
    logger.debug(f"{p_hash}: {[]}")
    redis.set(key=p_hash, value=json.dumps({"solvable": "?", "last_updated": now}))
    # run the solver
    # redis.set("", datetime.utcnow().isoformat())
    # redis.set("", datetime.utcnow().isoformat())
