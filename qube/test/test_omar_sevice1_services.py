#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['OMAR_SEVICE1_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['OMAR_SEVICE1_MONGOALCHEMY_SERVER'] = ''
    os.environ['OMAR_SEVICE1_MONGOALCHEMY_PORT'] = ''
    os.environ['OMAR_SEVICE1_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.omar_sevice1 import omar_sevice1
    from qube.src.services.omar_sevice1service import omar_sevice1Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, omar_sevice1ServiceError


class Testomar_sevice1Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.omar_sevice1Service = omar_sevice1Service(context)
        self.omar_sevice1_api_model = self.createTestModelData()
        self.omar_sevice1_data = self.setupDatabaseRecords(self.omar_sevice1_api_model)
        self.omar_sevice1_someoneelses = \
            self.setupDatabaseRecords(self.omar_sevice1_api_model)
        self.omar_sevice1_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.omar_sevice1_someoneelses.save()
        self.omar_sevice1_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.omar_sevice1_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.omar_sevice1_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, omar_sevice1_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            omar_sevice1_data = omar_sevice1(name='test_record')
            for key in omar_sevice1_api_model:
                omar_sevice1_data.__setattr__(key, omar_sevice1_api_model[key])

            omar_sevice1_data.description = 'my short description'
            omar_sevice1_data.tenantId = "23432523452345"
            omar_sevice1_data.orgId = "987656789765670"
            omar_sevice1_data.createdBy = "1009009009988"
            omar_sevice1_data.modifiedBy = "1009009009988"
            omar_sevice1_data.createDate = str(int(time.time()))
            omar_sevice1_data.modifiedDate = str(int(time.time()))
            omar_sevice1_data.save()
            return omar_sevice1_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_omar_sevice1(self, *args, **kwargs):
        result = self.omar_sevice1Service.save(self.omar_sevice1_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.omar_sevice1_api_model['name'])
        omar_sevice1.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_omar_sevice1(self, *args, **kwargs):
        self.omar_sevice1_api_model['name'] = 'modified for put'
        id_to_find = str(self.omar_sevice1_data.mongo_id)
        result = self.omar_sevice1Service.update(
            self.omar_sevice1_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.omar_sevice1_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_omar_sevice1_description(self, *args, **kwargs):
        self.omar_sevice1_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.omar_sevice1_data.mongo_id)
        result = self.omar_sevice1Service.update(
            self.omar_sevice1_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.omar_sevice1_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omar_sevice1_item(self, *args, **kwargs):
        id_to_find = str(self.omar_sevice1_data.mongo_id)
        result = self.omar_sevice1Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omar_sevice1_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(omar_sevice1ServiceError):
            self.omar_sevice1Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omar_sevice1_list(self, *args, **kwargs):
        result_collection = self.omar_sevice1Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.omar_sevice1_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.omar_sevice1_data.mongo_id)
        with self.assertRaises(omar_sevice1ServiceError) as ex:
            self.omar_sevice1Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.omar_sevice1_data.mongo_id)
        self.omar_sevice1Service.auth_context.is_system_user = True
        self.omar_sevice1Service.delete(id_to_delete)
        with self.assertRaises(omar_sevice1ServiceError) as ex:
            self.omar_sevice1Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.omar_sevice1Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.omar_sevice1_someoneelses.mongo_id)
        with self.assertRaises(omar_sevice1ServiceError):
            self.omar_sevice1Service.delete(id_to_delete)
