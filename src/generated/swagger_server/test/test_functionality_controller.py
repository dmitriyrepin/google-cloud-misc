# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestFunctionalityController(BaseTestCase):
    """FunctionalityController integration test stubs"""

    def test_put_busy(self):
        """Test case for put_busy

        Performs a high-CPU-usage request that is processed for 'duration' of seconds
        """
        response = self.client.open(
            '/v1/busy/{duration}'.format(duration=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_wait(self):
        """Test case for put_wait

        Performs a request that results in a wait for 'duration' of seconds
        """
        response = self.client.open(
            '/v1/wait/{duration}'.format(duration=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
