#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testomar_sevice1Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_omar_sevice1_model(self):
        from qube.src.models.omar_sevice1 import omar_sevice1
        omar_sevice1_data = omar_sevice1(name='testname')
        omar_sevice1_data.tenantId = "23432523452345"
        omar_sevice1_data.orgId = "987656789765670"
        omar_sevice1_data.createdBy = "1009009009988"
        omar_sevice1_data.modifiedBy = "1009009009988"
        omar_sevice1_data.createDate = str(int(time.time()))
        omar_sevice1_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            omar_sevice1_data.save()
            self.assertIsNotNone(omar_sevice1_data.mongo_id)
            omar_sevice1_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
