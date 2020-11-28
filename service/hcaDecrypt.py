# -*- coding:utf-8 -*-
import sys
import os
import time
from window.window_main import window_main
from service.decryptMaster import DecryptMaster
from math import ceil
from PyQt5.QtWidgets import QApplication
from typing import List

class hca_decrypt(DecryptMaster):
    """docstring for hca_decrypt"""
    def __init__(self):
        super(hca_decrypt, self).__init__()
        self.window_selectKey = window_main
        self.keyFile = self.hcaKeyFile

    def decrypt(self, app: QApplication, path: str) -> List[str]:
        self.set_progress(0)
        if self.key is None:
            self.key = self.select_key(app, 'HCA')
        if self.key == '00000000000022CE' and self.isParentFile(path):
            self.marge_files(self.search_marge_target(path))
        self.explode_acb(path)
        files_file = self.get_hca_files(path)
        if len(files_file) == 0:
            return []
        self.hca_decrypt(files_file)
        self.hca_decode(files_file)
        return self.rename_wav_file(path, files_file)

    def explode_acb(self, path):
        with open(path , 'rb') as f:
            if b'AFS2' == f.read(4):
                cmd = [self.afs2ExePath, path]
            else:
                cmd = [self.afs2ExeCutHeadPath, path]
        self.command(cmd)

    def hca_decrypt(self, fileList):
        allcount = len(fileList)
        count = 0
        for file in fileList:
            self.command([self.hcaDecryptPath, self.key, file])
            count = count + 1
            self.set_progress(ceil(count / allcount * 25))

    def hca_decode(self, fileList):
        count = 0
        allcount = len(fileList)
        for file in fileList:
            self.command([self.hcaDecodeExePath, file])
            count = count + 1
            self.set_progress(25 + ceil(count / allcount * 25))

    def get_hca_files(self, path):
        folderName = os.path.splitext(os.path.basename(path))[0]
        self.tmpDir = self.afs2Dir + '\\' + folderName
        try:
            files = os.listdir(self.tmpDir)
        except Exception as e:
            self.error(str(e))
            self.errorFiles.append(path)
            print("このファイルはスキップします。")
            self.progress = 100
            return []
        files_file_extnotchecked = [os.path.join(self.tmpDir, f) for f in files if os.path.isfile(os.path.join(self.tmpDir, f))]
        files_file = []
        for file in files_file_extnotchecked:
            if os.path.splitext(file)[1] in [".hca"]:
                files_file.append(file)
        return files_file

    def search_marge_target(self, path):
        if path.endswith('.acb'):
            ext = '.acb'
        elif path.endswith('acb.txt'):
            ext = 'acb.txt'
        else:
            return []
        spl = path.split('-')
        spl.reverse()
        count = spl[0][0:len(spl[0]) - len(ext)]
        fillCount = len(count)
        prefix = path[0:len(path) - len(count) - len(ext)]
        count = int(count)
        pathList = []
        while os.path.isfile(path):
            pathList.append(path)
            count = count + 1
            path = prefix + str(count).zfill(fillCount) + ext
        return pathList

    def marge_files(self, pathList):
        try:
            fin = pathList[0]
        except:
            return
        with open(fin, 'ab') as f:
            pathList.pop(0)
            print(fin + ' <----- ' + str(pathList))
            for path in pathList:
                with open(path, 'rb') as fi:
                    f.write(fi.read())
                self.command(['del', path])
                self.passPathList.append(path)
        return fin

    def isParentFile(self, path):
        if path.endswith('.acb'):
            path = path[0:len(path) - len('.acb')]
        elif path.endswith('.acb.txt'):
            path = path[0:len(path) - len('.acb.txt')]
        pathList = path.split('-')
        if len(pathList) > 1:
            c = pathList[len(pathList) - 1]
            try:
                return c.isdecimal()
            except:
                return False
