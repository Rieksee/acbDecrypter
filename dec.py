# -*- coding:utf-8 -*-
import sys
import os
from math import ceil
from window_progress import window_progress
from subprocess import DEVNULL, STDOUT, check_call

class Decrypt(object):
    """docstring for Decrypt"""
    def __init__(self, pathList, key, folderPath=None):
        super(Decrypt, self).__init__()
        self.window_progress = window_progress()
        self.window_progress.show()
        self.thisFileDir = self.get_path()
        self.key = key
        print("鍵に " + key + " を使用")
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
                if key == '00000000000022CE' and self.isParentFile(path):
                    self.marge_files(self.search_marge_target(path))
                if folderPath is not None:
                    relative = path[len(self.folderPath):]
                    prefix = os.path.dirname(relative).replace("/", self.separator) + os.path.basename(relative)
                    if len(prefix) > 0:
                        prefix = prefix + self.separator
                    self.decrypt(path, self.saveFolderPath, prefix)
                else:
                    self.decrypt(path)
            count = count + 1
            self.window_progress.setval(0, ceil(count / self.filesAllcount * 100))
            print(str(count) + '/' + str(self.filesAllcount) + 'ファイル完了')
            print('-' * 20)
        self.window_progress.close()
        print("エラー数:" + str(len(self.errorFiles)))
        print(self.errorFiles)
        print('全て完了しました。')
        if self.folderPath != "":
            os.system('explorer ' + self.saveFolderPath)

    def decrypt(self, path, savePath='', saveFileNamePrefix=''):
        self.window_progress.setval(1, 0)
        if savePath == '':
            resultDir = os.path.splitext(path)[0]
        else:
            resultDir = savePath
        self.command(['mkdir', resultDir])
        afs2Dir = self.thisFileDir + '\\acbToHca'
        afs2ExePath = afs2Dir + '\\afs2.exe'
        afs2ExeCutHeadPath = afs2Dir + '\\先頭をカットして展開.bat'
        hcaDecodeDir = self.thisFileDir + '\\hcaToWav'
        hcaDecryptPath = hcaDecodeDir + '\\復号化.bat'
        hcaDecodeExePath = hcaDecodeDir + '\\hca.exe'
        with open(path , 'rb') as f:
            if b'AFS2' == f.read(4):
                cmd = [afs2ExePath, path]
            else:
                cmd = [afs2ExeCutHeadPath, path]
        self.command(cmd)
        folderName = os.path.splitext(os.path.basename(path))[0]
        hcasDir = afs2Dir + '\\' + folderName
        try:
            files = os.listdir(hcasDir)
        except Exception as e:
            self.error(str(e))
            self.errorFiles.append(path)
            print("このファイルはスキップします。")
            self.window_progress.setval(1, 100)
            return
        files_file = [os.path.join(hcasDir, f) for f in files if os.path.isfile(os.path.join(hcasDir, f))]
        allcount = len(files_file)
        count = 0
        for file in files_file:
            self.command([hcaDecryptPath, self.key, file])
            count = count + 1
            if count % self.fileProgressShowCount == 0:
                self.window_progress.setval(1, 0 + ceil(count / allcount * 25))
        count = 0
        allcount = len(files_file)
        for file in files_file:
            self.command([hcaDecodeExePath, file])
            count = count + 1
            if count % self.fileProgressShowCount == 0:
                self.window_progress.setval(1, 25 + ceil(count / allcount * 25))
        wavFileNames = [os.path.splitext(file)[0] + '.wav' for file in files_file]
        count = 0
        newFileNames = []
        filenames = self.get_filename(path)
        allcount = len(wavFileNames)
        count = 0
        if len(filenames) == allcount:
            for file in wavFileNames:
                new = os.path.join(hcasDir, filenames[count].decode('utf-8') + '.wav')
                newFileNames.append(new)
                self.command(['move', file, new])
                count = count + 1
                if count % self.fileProgressShowCount == 0:
                    self.window_progress.setval(1, 50 + ceil(count / allcount * 25))
        else:
            newFileNames = wavFileNames
            print('wavファイル名候補数と実際のファイル数が異なっています。リネームを取りやめます。')
            self.window_progress.setval(1, 75)
        count = 0
        allcount = len(newFileNames)
        for fileName in newFileNames:
            baseName = os.path.basename(fileName)
            newname = resultDir + '/' + saveFileNamePrefix + baseName
            if os.path.isfile(newname):
                # print("ファイル名が重複しています。")
                # print(newname + "を")
                newname = self.rename(newname)
                # print(newname + "にリネームして保存します。")
            self.command(['move', fileName, newname])
            count = count + 1
            if count % self.fileProgressShowCount == 0:
                self.window_progress.setval(1, 75 + ceil(count / allcount * 25))
        self.window_progress.setval(1, 100)
        self.command(['rd', '/s', '/q', hcasDir])
        if self.folderPath == "":
            os.system('explorer ' + resultDir)

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

    def rename(self, name):
        count = 1
        tmpname = name
        ext = os.path.splitext(name)[1]
        name = os.path.splitext(name)[0]
        while os.path.isfile(tmpname):
            tmpname = name + "-" + str(count) + ext
            count = count + 1
        return tmpname

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
                    print("\nfailed the get file name")
                    dataoffset = None
                    break
                offset = offset + readLen + back
            return dataoffset

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
            return stri.split('\x00'.encode('ascii'))

    def error(self, e=None):
        print("エラーが発生しました。")
        if e is not None:
            print(e)

    def command(self, attr):
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except:
            return False

    def search_marge_target(self, path):
        if path.endswith('.acb'):
            ext = '.acb'
        elif path.endswith('.acb.txt'):
            ext = '.acb.txt'
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
