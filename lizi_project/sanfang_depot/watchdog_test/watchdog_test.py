#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : watchdog_test.py
# @Author: Lizi
# @Date  : 2020/12/7

from __future__ import print_function
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileSystemEventHandler
import time

WATCH_PATH = 'D:'


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(FileSystemEventHandler, self).__init__(**kwargs)
        self._watch_path = WATCH_PATH

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f'文件改变：{file_path}')
