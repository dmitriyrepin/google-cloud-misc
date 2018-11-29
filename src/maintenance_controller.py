"""For up-to-date function descriptions see 
generated/swagger_server/controllers/maintenance_controller.py
"""
import time
import logging
import os

_logger = logging.getLogger("drepin-service")

_version = None


def get_status():

    global _version

    if not _version:
        this_file_dir = os.path.dirname(__file__)
        file_path = os.path.join(this_file_dir, "../../build_version.txt")
        with open(file_path, "r") as f:
            _version = f.read()
    return "The service version: {}".format(_version)

def _print_headers(headers):
    print("")
    print("Headers:")
    for (key, value) in headers.items():
        print("   {}: {}".format(key, value))

def put_busy(duration, headers):
    # debug = "YES"
    debug = os.environ.get("DREPIN_DEBUG")
    message = "DREPIN_DEBUG is not defined. Delay duration: 0 sec."
    if debug:
        _print_headers(headers)
        message = "Delay duration: {} sec.".format(duration)
        now_sec = time.time()
        end_sec = now_sec + duration
        while now_sec < end_sec:
            now_sec = time.time()
    return message


def put_wait(duration, headers):
    # debug = "YES"
    debug = os.environ.get("DREPIN_DEBUG")
    message = "DREPIN_DEBUG is not defined. Delay duration: 0 sec."
    if debug:
        _print_headers(headers)
        message = "Delay duration: {} sec.".format(duration)
        time.sleep(duration)
    return message
