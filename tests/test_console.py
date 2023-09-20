#!/usr/bin/python3
""" console test suite """

import os
import pep8
import sys
from unittest.mock import create_autospec
from io import StringIO
import models
import unittest
from console import HBNBCommand


class test_console(unittest.TestCase):
    """class test console"""

    def test_pep8_console(self):
        """pep8 for console"""
        style = pep8.StyleGuide(quiet=False)
        errors = 0
        file = (["console.py"])
        errors += style.check_files(file).total_errors
        self.assertEqual(errors, 0, 'Need to fix Pep8')

    def setUp(self):
        """ setup """
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out

    def tearDown(self):
        """ teardown """
        sys.stdout = self.backup

    def create(self):
        """ create HBNBCommand class """
        return HBNBCommand()

    def test_quit(self):
        """quit test """
        console = self.create()
        self.assertTrue(console.onecmd("quit"))

    def test_EOF(self):
        """ test eof """
        console = self.create()
        self.assertTrue(console.onecmd("EOF"))

    def test_all(self):
        """ test all """
        console = self.create()
        console.onecmd("all")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "won't work in db")
    def test_show(self):
        """ tests show """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show User " + user_id)
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertTrue(isinstance(x, str))

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "won't work in db")
    def test_show_class_name(self):
        """ test show class name """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** class name missing **\n", x)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "won't work in db")
    def test_show_class_name(self):
        """ test show class name """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show User")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** instance id missing **\n", x)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "won't work in db")
    def test_show_no_instance_found(self):
        """ test show no instance found """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show User " + "124356876")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** no instance found **\n", x)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "won't work in db")
    def test_create_fileStorage(self):
        """ test create file stroge """
        console = self.create()
        console.onecmd("create User")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_class_name(self):
        """ test class name """
        console = self.create()
        console.onecmd("create")
        x = (self.capt_out.getvalue())
        self.assertEqual("** class name missing **\n", x)

    def test_class_name_doest_exist(self):
        """ tests class name doesnt exist """
        console = self.create()
        console.onecmd("create Binita")
        x = (self.capt_out.getvalue())
        self.assertEqual("** class doesn't exist **\n", x)
