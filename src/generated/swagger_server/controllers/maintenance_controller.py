# import connexion
# import six
# pylint: disable=no-name-in-module
from service import controllers as impl
# pylint: enable=no-name-in-module

def get_healthz():
    """Health check

    Returns:
        str: Always returns "200"
    """
    return "OK"


def get_status():
    """Returns the server status

    Returns:
        str: service status string, including service version
    """
    return impl.get_status()
