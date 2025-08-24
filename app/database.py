from redis import Redis
r = Redis(host="redis", port=6379, decode_responses=True)