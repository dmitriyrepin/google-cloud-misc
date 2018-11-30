# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestMaintenanceController(BaseTestCase):
    """MaintenanceController integration test stubs"""

    def test_get_healthz(self):
        """Test case for get_healthz

        Health check
        """
        response = self.client.open(
            '/v1/healthz',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_status(self):
        """Test case for get_status

        Returns the server status
        """
        response = self.client.open(
            '/v1/status',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
