# -*- coding:utf-8 -*-
import sys
import os
import time
from math import ceil
from window_main import window_main
from subprocess import DEVNULL, STDOUT, check_call
from PyQt5.QtWidgets import QApplication

class hca_decrypt(object):
    """docstring for hca_decrypt"""
    def __init__(self, progressBar=None):
        self.progressBar = progressBar
        super(hca_decrypt, self).__init__()
        self.key = None
        self.progress = 0
        self.hcasDir = ""
        self.thisFileDir = self.get_path()
        self.afs2Dir = self.thisFileDir + '\\acbToHca'
        self.afs2ExePath = self.afs2Dir + '\\afs2.exe'
        self.afs2ExeCutHeadPath = self.afs2Dir + '\\先頭をカットして展開.bat'
        self.hcaDecodeDir = self.thisFileDir + '\\hcaToWav'
        self.hcaDecryptPath = self.hcaDecodeDir + '\\復号化.bat'
        self.hcaDecodeExePath = self.hcaDecodeDir + '\\hca.exe'
        self.keyFile = self.hcaDecodeDir + "\\復号鍵リスト.txt"
        self.errorFiles = []


    def decrypt(self, app, path):
        self.set_progress(0)
        if self.key is None:
            self.key = self.select_key(app)
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

    def command(self, attr):
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except Exception as e:
            self.error(e)
            return False

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

    def rename_wav_file(self, path, files_file):
        filenames = self.get_wav_file_names(path, files_file)
        if self.can_get_wav_file_name(filenames):
            newFileNames = []
            allcount = len(filenames[1])
            count = 0
            for file in filenames[0]:
                new = os.path.join(self.hcasDir, filenames[1][count] + '.wav')
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

        # 調査したのがawbファイルで元ファイル名が見つからない場合acbファイルも調査する
        if len(filenames) == 0 and self.awb_file(path) != 0:
            if self.awb_file(path) == 1:
                filenames = self.get_filename(os.path.splitext(path)[0] + ".acb")
            elif self.awb_file(path) == 2:
                acbpath = path[:len(path) - len('awb.txt')] + 'acb.txt'
                filenames = self.get_filename(acbpath)

        return [wavFileNames, filenames]

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

    def get_hca_files(self, path):
        folderName = os.path.splitext(os.path.basename(path))[0]
        self.hcasDir = self.afs2Dir + '\\' + folderName
        try:
            files = os.listdir(self.hcasDir)
        except Exception as e:
            self.error(str(e))
            self.errorFiles.append(path)
            print("このファイルはスキップします。")
            self.progress = 100
            return []
        files_file_extnotchecked = [os.path.join(self.hcasDir, f) for f in files if os.path.isfile(os.path.join(self.hcasDir, f))]
        files_file = []
        for file in files_file_extnotchecked:
            if os.path.splitext(file)[1] in [".hca"]:
                files_file.append(file)
        return files_file

    def select_key(self, app):
        print('HCAファイルが見つかりました。鍵を選択してください。')
        self.window_main = window_main(self.keyFile)
        self.window_main.show()
        app.exec_()
        while self.window_main.get_key() is None:
            time.sleep(5)
        key = self.window_main.get_key()
        if key == "":
            print("HCA用鍵なし")
        else:
            print("HCA用鍵に" + key + "を使用")
        return key

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

    def error(self, e=None):
        if e is not None:
            print("Error: " + str(e))

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

    def get_error_files(self):
        return self.errorFiles

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

    def get_progress(self):
        return self.progress

    def set_progress(self, level):
        self.progress = level
        if self.progressBar is not None:
            self.progressBar.setval(1, level)

    def get_tmp_dir(self):
        return self.hcasDir

    def awb_file(self, path):
        if os.path.splitext(os.path.basename(path))[1].lower() == ".awb":
            return 1
        elif os.path.basename(path).lower().endswith("awb.txt"):
            return 2
        else:
            return 0
