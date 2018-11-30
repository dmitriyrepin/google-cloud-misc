#!/usr/bin/env python3
import logging
import connexion
from swagger_server import encoder

_logger = logging.getLogger("drepin-service")
_logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('   %(levelname)s[%(name)s]: %(message)s'))
_logger.addHandler(_handler)


def application():
    _app = connexion.App(__name__, specification_dir='./generated/swagger_server/swagger')
    _app.app.json_encoder = encoder.JSONEncoder
    _app.add_api('swagger.yaml', arguments={'title': 'Sample Web Service'})
    return _app


app = application()

if __name__ == '__main__':
    app.run(port=8080)
