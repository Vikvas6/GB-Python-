import logging
from functools import wraps

logger = logging.getLogger('server.decorators')


def logged(log_format):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            response = func(request)
            logger.debug(
                log_format % {'name': func.__name__, 'request': request, 'response': response})
            return response
        return wrapper
    return decorator
