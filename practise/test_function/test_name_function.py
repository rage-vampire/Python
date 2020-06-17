# -*- coding:utf-8 -*-
# Filename: test_name_function.py
# Author: Lizi
# Time: 2019/12/21 17:45

import unittest
from name_function import get_name

class NamesTestCase(unittest.TestCase):
    def test_f_l_name(self):
        formatted_name = get_name("janins",'joplin')
        self.assertEqual(formatted_name,'Janins Joplin')

    def test_f_l_m_name(self):
        formatted_name = get_name("wolfgang",'mozart','adameus')
        self.assertEqual(formatted_name,'Wolfgang Adameus Mozart')
unittest.main()