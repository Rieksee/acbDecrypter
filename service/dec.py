# -*- coding:utf-8 -*-
import sys
import os
import time
from math import ceil
from window.window_adxKeySelect import window_adxKeySelect
from subprocess import DEVNULL, STDOUT, check_call
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from service.hcaDecrypt import hca_decrypt
from service.adxDecrypt import adx_decrypt

class Decrypt(QtCore.QThread):
    """docstring for Decrypt"""
    def __init__(self, app, progress, pathList, folderPath=None):
        super(Decrypt, self).__init__()
        self.app = app
        self.window_progress = progress
        self.hcaDecrypt = hca_decrypt(self.window_progress)
        self.adxDecrypt = adx_decrypt(self.window_progress)
        self.thisFileDir = self.get_path()

        self.adxKey = None

        self.separator = '_'
        self.passPathList = []
        self.fileProgressShowCount = 2
        if folderPath is not None:
            self.saveFolderPath = folderPath + "_decrypted"
            self.folderPath = folderPath
        else:
            self.folderPath = ''
            self.saveFolderPath = ''
        count = 0
        self.errorFiles = []
        count = 0
        self.filesAllcount = len(pathList)
        for path in pathList:
            if path not in self.passPathList:
                if folderPath is not None:
                    relative = path[len(self.folderPath):]
                    prefix = os.path.dirname(relative).replace("/", self.separator) + self.separator + os.path.basename(relative)
                    if len(prefix) > 0:
                        prefix = prefix + self.separator
                    self.decrypt(path, self.saveFolderPath, prefix)
                else:
                    self.decrypt(path)
            count = count + 1
            self.window_progress.setval(0, ceil(count / self.filesAllcount * 100))
            print(str(count) + '/' + str(self.filesAllcount) + 'ファイル完了')
            print('-' * 20)
        self.window_progress.finish()
        print("エラー数:" + str(len(self.errorFiles)))
        print(self.errorFiles)
        print('全て完了しました。')
        if self.folderPath != "":
            os.system('explorer ' + self.saveFolderPath)
        self.finished.emit()

    def decrypt(self, path, savePath='', saveFileNamePrefix=''):
        # self.window_progress.setval(1, 0)
        if savePath == '':
            resultDir = os.path.splitext(path)[0]
        else:
            resultDir = savePath
        if not os.path.isdir(resultDir):
            self.command(['mkdir', resultDir])
        
        if self.is_adx(path):
            newFileNames = self.adxDecrypt.decrypt(self.app, path)
            self.errorFiles.extend(self.adxDecrypt.get_error_files())
            self.move_wav_file(newFileNames, resultDir, saveFileNamePrefix)
            self.command(['rd', '/s', '/q', self.adxDecrypt.get_tmp_dir()])
        else:
            newFileNames = self.hcaDecrypt.decrypt(self.app, path)
            self.errorFiles.extend(self.hcaDecrypt.get_error_files())
            self.move_wav_file(newFileNames, resultDir, saveFileNamePrefix)
            self.command(['rd', '/s', '/q', self.hcaDecrypt.get_tmp_dir()])

        self.window_progress.setval(1, 100)
        if self.folderPath == "":
            os.system('explorer ' + resultDir)

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

    def chk_file_type(self, file):
        # types:
        #     1 hca
        #     2 adx
        copylight = '(c)CRI'
        offset = self.findStr(file, copylight, 0, -len(copylight), 1)
        if offset is None:
            return 1
        else:
            return 2

    def is_adx(self, file):
        if self.chk_file_type(file) == 2:
            return True
        else:
            return False

    def error(self, e=None):
        if e is not None:
            print("Error: " + str(e))

    def command(self, attr):
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except Exception as e:
            self.error(e)
            return False

    def move_wav_file(self, newFileNames, resultDir, saveFileNamePrefix):
        count = 0
        allcount = len(newFileNames)
        for fileName in newFileNames:
            baseName = os.path.basename(fileName)
            newname = resultDir + '\\' + saveFileNamePrefix + baseName
            if os.path.isfile(newname):
                newname = self.rename(newname)
            self.command(['move', fileName, newname])
            count = count + 1
            self.setProgress(75 + ceil(count / allcount * 25))

    def findStr(self, file, searchStr, offset, back, count):
        filesize = os.path.getsize(file)
        readLen = 40
        with open(file, 'rb') as f:
            while True:
                f.seek(offset)
                data = f.read(readLen)
                findAt = data.find(searchStr.encode('ascii'))
                if findAt != -1:
                    dataoffset = findAt + offset
                    count = count - 1
                    if count <= 0:
                        break
                if offset + readLen > filesize:
                    dataoffset = None
                    break
                offset = offset + readLen + back
            return dataoffset

    def decryptAdx(self, path):
        self.newFileNames = self.adxDecrypt.decrypt(path)

    def decryptHca(self, path):
        self.newFileNames = self.hcaDecrypt.decrypt(path)

    def getProgress(self, resource):
        while True:
            progress = resource.get_progress()
            self.setProgress(progress)
            time.sleep(0.5)

    def setProgress(self, level, bar=1):
        self.window_progress.setval(bar, level)

    def rename(self, name):
        count = 1
        tmpname = name
        ext = os.path.splitext(name)[1]
        name = os.path.splitext(name)[0]
        while os.path.isfile(tmpname):
            tmpname = name + "-" + str(count) + ext
            count = count + 1
        return tmpname
