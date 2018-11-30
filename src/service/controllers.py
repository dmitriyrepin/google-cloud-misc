"""Hand-codded bodies of the generated controllers. 
See generated/swagger_server/controllers/
"""
import time
import logging
import os

_logger = logging.getLogger("drepin-service")

_version = None

def _print_headers(headers):
    print("")
    print("Headers:")
    for (key, value) in headers.items():
        print("   {}: {}".format(key, value))

def get_status():
    """Returns the server status

    Returns:
        str: service status string, including service version
    """

    # pylint: disable=global-statement
    global _version
    # pylint: global-statement

    if not _version:
        this_file_dir = os.path.dirname(__file__)
        file_path = os.path.join(this_file_dir, "../../build_version.txt")
        with open(file_path, "r") as f:
            _version = f.read()

        # _print_headers(headers)
    return "The service version: {}".format(_version)

def put_busy(duration, headers):
    """Performs a high-CPU-usage request that is processed for 'duration' of seconds

    Args:
        duration (int): The request processing duration (seconds).

    Returns:
        str: Always returns "200"

    """
    debug = os.environ.get("DREPIN_DEBUG")
    message = "DREPIN_DEBUG is not defined. Delay duration: 0 sec."
    if debug:
        message = "Delay duration: {} sec.".format(duration)
        now_sec = time.time()
        end_sec = now_sec + duration
        while now_sec < end_sec:
            now_sec = time.time()
    return message


def put_wait(duration, headers):
    """Performs a request that results in a wait for 'duration' of seconds

    Args:
        duration (int): The request processing duration (seconds).

    Returns:
        str: Always returns "200"
    """
    debug = os.environ.get("DREPIN_DEBUG")
    message = "DREPIN_DEBUG is not defined. Delay duration: 0 sec."
    if debug:
        message = "Delay duration: {} sec.".format(duration)
        time.sleep(duration)
    return message
