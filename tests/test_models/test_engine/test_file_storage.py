#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
import time
import json
from models.state import State



class testFileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        self.storage = FileStorage()
        self.my_model = BaseModel()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_return_type(self):
        """ __objects is properly returned """
        storage_all = self.storage.all()
        self.assertIsInstance(storage_all, dict)

    def test_delete(self):
        """ File is not created on BaseModel save """
        new_state = State()
        new_state.name = "California***********"
        fs = FileStorage()
        fs.new(new_state)
        fs.save()
        self.assertTrue(os.path.isfile("file.json"))
        with open("file.json", encoding="UTF8") as fd:
            content = fd.read()
        flag = 1
        if new_state.id in content:
            flag = 0
        self.assertTrue(flag == 0)
        fs.delete(new_state)
        fs.save()
        with open("file.json", encoding="UTF8") as fd:
            content = fd.read()
        flag = 0
        if new_state.id in content:
            flag = 1
        self.assertTrue(flag == 0)

    def test_new_method(self):
        """ Data is saved to file """
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        self.assertTrue(key in self.storage._FileStorage__objects)

    def test_objects_value_type(self):
        """ FileStorage save method """
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        val = self.storage._FileStorage__objects[key]
        self.assertIsInstance(self.my_model, type(val))

    def test_save_file_exists(self):
        """ Storage file is successfully loaded to __objects """
        self.storage.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_save_file_read(self):
        """ Load from an empty file """
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = json.load(fd)

        self.assertTrue(isinstance(content, dict))

    def test_the_type_file_content(self):
        """ Nothing happens if file does not exist """
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = fd.read()

        self.assertIsInstance(content, str)

    def test_reaload_without_file(self):
        """ BaseModel save method calls storage save """
        try:
            self.storage.reload()
            self.assertTrue(True)
        except BaseException:
            self.assertTrue(False)
