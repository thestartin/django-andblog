from functools import wraps
from ipware.ip import get_real_ip


def get_ip_hashed(view_func):
    @wraps(view_func)
    def hash_ip(self, request, *args, **kwargs):
        ip = get_real_ip(request)
        if ip is not None:
            # we have a real, public ip address for user
            hashed_ip = hash(ip)
        else:
            # we don't have a real, public ip address for user
            hashed_ip = None
        return view_func(self, request, hashed_ip, *args, **kwargs)

    return hash_ip