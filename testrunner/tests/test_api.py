import json

from datetime import datetime

from testrunner.models import (
    Environment,
    Request,
    )

from testrunner.tests.test_base import BaseTestCase


class TestRequest(BaseTestCase):
    def test_api(self):
        created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        response = self.simulate_request(
            '/api/environment/', method='POST',
            body=json.dumps({
                'name': 'Test Environment'
            }),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
        self.assertCreated(response)

        response = self.simulate_request(
            '/api/request/', method='POST',
            body=json.dumps({
                'requester': 'Bob',
                'environment_id': 1,
                'files': '["testA.py", "testB.py"]',
                'output': None,
                'created': created
            }),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
        self.assertCreated(response)

        response, = self.simulate_request(
            '/api/request/', method='GET',
            headers={
                'Accept': 'application/json'
            })
        self.assertOK(response, {
            'data': [{
                'id': 1,
                'requester': 'Bob',
                'environment_id': 1,
                'state': 'PENDING',
                'files': '["testA.py", "testB.py"]',
                'output': None,
                'created': created
            }]
        })

        response, = self.simulate_request(
            '/api/request/1', method='GET',
            headers={
                'Accept': 'application/json'
            })
        self.assertOK(response, {
            'data': {
                'id': 1,
                'requester': 'Bob',
                'environment_id': 1,
                'state': 'PENDING',
                'files': '["testA.py", "testB.py"]',
                'output': None,
                'created': created
            }
        })
