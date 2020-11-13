# -*- coding: utf-8 -*-

import os
import sys
import time
from math import ceil
from service.decryptMaster import DecryptMaster
from window.window_adxKeySelect import window_adxKeySelect
from PyQt5.QtWidgets import QApplication

class adx_decrypt(DecryptMaster):
    """docstring for adx_decrypt"""
    def __init__(self, progressBar=None):
        super(adx_decrypt, self).__init__(progressBar)
        self.tmpPath = ""
        self.keyFile = self.adxSpecialKeyList
        self.window_selectKey = window_adxKeySelect
        
    def decrypt(self, app, path):
        self.set_progress(0)
        if self.key is None:
            self.key = self.select_key(app, 'ADX')
        tmpPath = self.acb_to_adx(path)
        self.tmpPath = tmpPath
        if tmpPath == "":
            self.error(path=path)
            self.set_progress(100)
            return []
        self.set_progress(25)
        res = self.decode_adx(app, tmpPath)
        self.set_progress(50)
        if not res:
            self.error(path=path)
            self.set_progress(100)
            return []
        return self.rename_wav_file(path, [res])

    def decode_adx(self, app, path):
        com = [self.adxSpecialDecryptPath, path, self.key]
        self.command(com)
        filename = os.path.splitext(path)[0] + '.wav'
        if os.path.isfile(filename):
            return filename
        else:
            return False

    def acb_to_adx(self, path):
        offset = self.findStr(path, 'AFS2', 0, -4, 1)
        offset = self.findByte(path, b'\x80\x00', offset, -2, 1)
        if offset is None:
            return ''
        self.tmpDir = self.get_path() + '\\tmp'
        self.command(['mkdir', self.tmpDir])
        with open(path, 'rb') as f:
            f.seek(offset)
            data = f.read()
        tmpPath = self.tmpDir + '\\' + os.path.basename(path)
        with open(tmpPath, 'wb') as f:
            f.write(data)
        return tmpPath

    def get_wav_file_names(self, path, fileList):
        # 連番の名前
        wavFileNames = [os.path.splitext(file)[0] + '.wav' for file in fileList]

        # acbファイルに格納されている元の名前
        filenames = self.get_filename(path)

        return [wavFileNames, filenames]

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))
