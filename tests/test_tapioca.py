#!/usr/bin/env python
# coding: utf-8

import unittest

import responses
import requests

from tests.client import TestTapiocaClient


class TestTapioca(unittest.TestCase):

    def setUp(self):
        self.wrapper = TestTapiocaClient()

    def test_resource_executor_data_should_be_composed_url(self):
        expected_url = 'https://api.test.com/test/'
        resource = self.wrapper.test()

        self.assertEqual(resource.data(), expected_url)

    @responses.activate
    def test_get_request(self):
        responses.add(responses.GET, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=200,
            content_type='application/json')

        response = self.wrapper.test().get()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_access_response_field(self):
        responses.add(responses.GET, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=200,
            content_type='application/json')

        response = self.wrapper.test().get()

        response_data = response.data()

        self.assertEqual(response_data.data(), {'key': 'value'})

    def test_fill_url_template(self):
        expected_url = 'https://api.test.com/user/123/'

        resource = self.wrapper.user(id='123')

        self.assertEqual(resource.data(), expected_url)

    @responses.activate
    def test_post_request(self):
        responses.add(responses.POST, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().post()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_put_request(self):
        responses.add(responses.PUT, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().put()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_patch_request(self):
        responses.add(responses.PATCH, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().patch()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_delete_request(self):
        responses.add(responses.DELETE, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().delete()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_simple_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data(),
            body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
            status=200,
            content_type='application/json')

        responses.add(responses.GET, next_url,
            body='{"data": [{"key": "value"}], "paging": {"next": ""}}',
            status=200,
            content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response:
            self.assertIn(item.key().data(), 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 2)

    def test_docs(self):
        self.assertEquals('\n'.join(self.wrapper.resource.__doc__.split('\n')[1:]),
                          'Resource: ' + self.wrapper.resource._resource['resource'] + '\n'
                          'Docs: ' + self.wrapper.resource._resource['docs'] + '\n'
                          'Foo: ' + self.wrapper.resource._resource['foo'] + '\n'
                          'Spam: ' + self.wrapper.resource._resource['spam'])

if __name__ == '__main__':
    unittest.main()
