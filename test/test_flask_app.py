import os
import unittest
from flask import Flask, jsonify
import urllib2
import voc
from flask_testing import TestCase
from flask_testing import LiveServerTestCase

class VoCTest(LiveServerTestCase, TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 3000

        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_product_list(self):
        response = voc.get_product_list()
        self.assertTrue(len(response.json) > 0)


if __name__ == '__main__':
    unittest.main()
