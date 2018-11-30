import connexion
# import six

# from swagger_server import util

# pylint: disable=no-name-in-module
from service import controllers as impl
# pylint: enable=no-name-in-module

def put_busy(duration):
    """Performs a high-CPU-usage request that is processed for 'duration' of seconds

    Args:
        duration (int): The request processing duration (seconds).

    Returns:
        str: Always returns "200"

    """
    headers = connexion.request.headers
    return impl.put_busy(duration, headers)


def put_wait(duration):
    """Performs a request that results in a wait for 'duration' of seconds

    Args:
        duration (int): The request processing duration (seconds).

    Returns:
        str: Always returns "200"
    """
    headers = connexion.request.headers
    return impl.put_wait(duration, headers)
