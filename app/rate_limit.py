from database import r

RATE_LIMIT = 5
WINDOW = 60

def is_rate_limited(client_ip) -> bool:
    key = f"rate_limit:{client_ip}"
    current_count = r.get(key)
    if current_count is None:
        r.set(key, 1, ex=WINDOW)
        return False
    elif int(current_count) < RATE_LIMIT:
        r.incr(key)
        return False
    else:
        return True