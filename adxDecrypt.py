# -*- coding: utf-8 -*-

import os
import sys
import time
from math import ceil
from subprocess import DEVNULL, STDOUT, check_call
from window_adxKeySelect import window_adxKeySelect
from PyQt5.QtWidgets import QApplication

class adx_decrypt(object):
    """docstring for adx_decrypt"""
    def __init__(self, progressBar=None):
        super(adx_decrypt, self).__init__()
        if progressBar is not None:
            self.progressBar = progressBar
        self.key = None
        self.tmpPath = ""
        self.errorFiles = []
        self.progress = 0
        self.thisFileDir = self.get_path()
        self.adxDecryptDir = self.thisFileDir + '\\adxToWav'
        self.adxSpecialDecryptPath = self.adxDecryptDir + '\\特殊鍵指定デコード.bat'
        self.adxSpecialKeyList = self.adxDecryptDir + '\\特殊鍵リスト.txt'
        self.adxDecryptPath = self.adxDecryptDir + '\\復号鍵指定デコード.bat'
        self.adxKeyList = self.adxDecryptDir + '\\復号鍵リスト.txt'
        
    def decrypt(self, app, path):
        self.set_progress(0)
        if self.key is None:
            self.key = self.select_key(app)
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

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

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
        tmpDir = self.get_path() + '\\tmp'
        self.command(['mkdir', tmpDir])
        with open(path, 'rb') as f:
            f.seek(offset)
            data = f.read()
        tmpPath = tmpDir + '\\' + os.path.basename(path)
        with open(tmpPath, 'wb') as f:
            f.write(data)
        return tmpPath

    def select_key(self, app):
        print('ADXファイルが見つかりました。鍵を選択してください。')
        adxKeySelect = window_adxKeySelect(self.adxSpecialKeyList)
        adxKeySelect.show()
        app.exec_()
        key = adxKeySelect.get_key()
        if key == "":
            print("ADX鍵なし")
        else:
            print("ADX鍵に" + key + "を使用")
        return key

    def error(self, e=None, path=None):
        if e is not None:
            print("Error: " + str(e))
        if path is not None:
            self.errorFiles.append(path)

    def command(self, attr):
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            time.sleep(2)
            return True
        except:
            return False

    def rename_wav_file(self, path, files_file):
        filenames = self.get_wav_file_names(path, files_file)
        if self.can_get_wav_file_name(filenames):
            newFileNames = []
            allcount = len(filenames[1])
            count = 0
            for file in filenames[0]:
                new = os.path.join(self.get_tmp_dir(), filenames[1][count] + '.wav')
                newFileNames.append(new)
                self.command(['move', file, new])
                count = count + 1
                self.set_progress(50 + ceil(count / allcount * 25))
        else:
            newFileNames = filenames[0]
            print('wavファイル名候補数と実際のファイル数が異なっています。リネームを取りやめます。')
            self.set_progress(75)
        return newFileNames

    def can_get_wav_file_name(self, nameLists):
        wavFileNames = nameLists[0]
        filenames = nameLists[1]
        if len(wavFileNames) > len(filenames):
            return False
        else:
            return True

    def get_wav_file_names(self, path, fileList):
        # 連番の名前
        wavFileNames = [os.path.splitext(file)[0] + '.wav' for file in fileList]

        # acbファイルに格納されている元の名前
        filenames = self.get_filename(path)

        return [wavFileNames, filenames]

    def get_filename(self, filename):
        offset = self.findStr(filename, '@UTF', 0, -4, 3)
        if offset is None:
            return []
        offset = self.findStr(filename, '\x00CueName\x00CueIndex\x00', offset, -20, 1)
        if offset is None:
            return []
        offset = offset + len('\x00CueName\x00CueIndex\x00')
        end = self.findStr(filename, '\x00\x00', offset, -4, 1)
        with open(filename, 'rb') as f:
            f.seek(offset)
            stri = f.read(end - offset)
            names = stri.split('\x00'.encode('ascii'))
        ret = []
        for name in names:
            ret.append(name.decode('utf-8'))
        return ret

    def get_error_files(self):
        return self.errorFiles

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

    def get_progress(self):
        return self.progress

    def set_progress(self, level):
        self.progress = level
        if self.progressBar is not None:
            self.progressBar.setval(1, level)

    def findStr(self, file, searchStr, offset, back, count):
        filesize = os.path.getsize(file)
        readLen = 40
        with open(file, 'rb') as f:
            while True:
                f.seek(offset)
                data = f.read(readLen)
                findAt = data.find(searchStr.encode('utf-8'))
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

    def findByte(self, file, searchByte, offset, back, count):
        filesize = os.path.getsize(file)
        readLen = 40
        search = None
        searchArray = bytearray(searchByte)
        with open(file, 'rb') as f:
            while True:
                f.seek(offset)
                data = f.read(readLen)
                matchCount = 0
                data = bytearray(data)
                dataCount = 0
                for bt in data:
                    if bt == searchArray[matchCount]:
                        # 一致したとき
                        if matchCount == 0:
                            findAt = dataCount
                        matchCount = matchCount + 1
                    else:
                        # 一致しない時
                        matchCount = 0
                    dataCount = dataCount + 1
                    if matchCount >= len(searchArray):
                        break
                else:
                    # 一致しないままreadしたdataを読み終わったとき
                    if offset + readLen > filesize:
                        # ファイルの最後まで読んでいるとき
                        dataoffset = None
                        break
                    offset = offset + readLen + back
                    continue
                dataoffset = findAt + offset
                count = count - 1
                if count <= 0:
                    break
            return dataoffset

    def get_tmp_dir(self):
        return os.path.dirname(self.tmpPath)
