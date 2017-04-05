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

        self.hcasDir = ""
        self.adxKey = None

        self.afs2Dir = self.thisFileDir + '\\acbToHca'
        self.afs2ExePath = self.afs2Dir + '\\afs2.exe'
        self.afs2ExeCutHeadPath = self.afs2Dir + '\\先頭をカットして展開.bat'
        self.hcaDecodeDir = self.thisFileDir + '\\hcaToWav'
        self.hcaDecryptPath = self.hcaDecodeDir + '\\復号化.bat'
        self.hcaDecodeExePath = self.hcaDecodeDir + '\\hca.exe'
        self.adxDecryptDir = self.thisFileDir + '\\adxToWav'
        self.adxDecryptPath = self.adxDecryptDir + '\\復号鍵指定デコード.bat'
        # self.adxDecryptKeyList = self.adxDecryptDir + '\\復号鍵リスト.txt'

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
                    prefix = os.path.dirname(relative).replace("/", self.separator) + self.separator + os.path.basename(relative)
                    if len(prefix) > 0:
                        prefix = prefix + self.separator
                    self.decrypt(path, self.saveFolderPath, prefix)
                else:
                    self.decrypt(path)
            count = count + 1
            self.window_progress.setval(0, ceil(count / self.filesAllcount * 100))
            # print(path)
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
        
        if self.is_adx(path):
            if self.adxKey is None:
                print('ADXファイルが見つかりました。鍵を入力してください。')
                self.adxKey = input('>>')
                if self.adxKey == "":
                    print('鍵なし')
                else:
                    print('鍵に' + self.adxKey + 'を使用')
            tmpPath = self.acb_to_adx(path)
            if tmpPath == "":
                self.error()
                self.errorFiles.append(path)
                self.command(['rd', '/s', '/q', os.path.dirname(tmpPath)])
                self.window_progress.setval(1, 100)
            self.window_progress.setval(1, 40)
            res = self.decode_adx(tmpPath)
            self.window_progress.setval(1, 80)
            if not res:
                self.error()
                self.errorFiles.append(path)
                self.command(['rd', '/s', '/q', os.path.dirname(tmpPath)])
                self.window_progress.setval(1, 100)
                return
            self.move_wav_file([res], resultDir, saveFileNamePrefix)
            self.command(['rd', '/s', '/q', os.path.dirname(tmpPath)])
        else:
            self.explode_acb(path)
            files_file = self.get_hca_files(path)
            self.hca_decrypt(files_file)
            self.hca_decode(files_file)
            newFileNames = self.rename_wav_file(path, files_file)
            self.move_wav_file(newFileNames, resultDir, saveFileNamePrefix)
            self.command(['rd', '/s', '/q', self.hcasDir])

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

    def awb_file(self, path):
        if os.path.splitext(os.path.basename(path))[1].lower() == ".awb":
            return 1
        elif os.path.basename(path).lower().endswith("awb.txt"):
            return 2
        else:
            return 0

    def hca_decrypt(self, fileList):
        allcount = len(fileList)
        count = 0
        for file in fileList:
            self.command([self.hcaDecryptPath, self.key, file])
            count = count + 1
            if count % self.fileProgressShowCount == 0:
                self.window_progress.setval(1, 0 + ceil(count / allcount * 25))

    def hca_decode(self, fileList):
        count = 0
        allcount = len(fileList)
        for file in fileList:
            self.command([self.hcaDecodeExePath, file])
            count = count + 1
            if count % self.fileProgressShowCount == 0:
                self.window_progress.setval(1, 25 + ceil(count / allcount * 25))

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

    def rename_wav_file(self, path, files_file):
        filenames = self.get_wav_file_names(path, files_file)
        if self.can_get_wav_file_name(filenames):
            newFileNames = filenames[1]
            allcount = len(newFileNames)
            count = 0
            for file in filenames[0]:
                new = os.path.join(self.hcasDir, newFileNames[count] + '.wav')
                newFileNames.append(new)
                self.command(['move', file, new])
                count = count + 1
                if count % self.fileProgressShowCount == 0:
                    self.window_progress.setval(1, 50 + ceil(count / allcount * 25))
        else:
            newFileNames = filenames[0]
            print('wavファイル名候補数と実際のファイル数が異なっています。リネームを取りやめます。')
            self.window_progress.setval(1, 75)
        return newFileNames

    def move_wav_file(self, newFileNames, resultDir, saveFileNamePrefix):
        count = 0
        allcount = len(newFileNames)
        for fileName in newFileNames:
            baseName = os.path.basename(fileName)
            newname = resultDir + '/' + saveFileNamePrefix + baseName
            if os.path.isfile(newname):
                newname = self.rename(newname)
            self.command(['move', fileName, newname])
            count = count + 1
            if count % self.fileProgressShowCount == 0:
                self.window_progress.setval(1, 75 + ceil(count / allcount * 25))

    def get_hca_files(self, path):
        folderName = os.path.splitext(os.path.basename(path))[0]
        self.hcasDir = self.afs2Dir + '\\' + folderName
        try:
            files = os.listdir(self.hcasDir)
        except Exception as e:
            self.error(str(e))
            self.errorFiles.append(path)
            print("このファイルはスキップします。")
            self.window_progress.setval(1, 100)
            return []
        files_file_extnotchecked = [os.path.join(self.hcasDir, f) for f in files if os.path.isfile(os.path.join(self.hcasDir, f))]
        files_file = []
        for file in files_file_extnotchecked:
            if os.path.splitext(file)[1] in [".hca"]:
                files_file.append(file)
        return files_file

    def explode_acb(self, path):
        with open(path , 'rb') as f:
            if b'AFS2' == f.read(4):
                cmd = [self.afs2ExePath, path]
            else:
                cmd = [self.afs2ExeCutHeadPath, path]
        self.command(cmd)

    def decode_adx(self, path):
        com = [self.adxDecryptPath, path, self.adxKey]
        self.command(com)
        filename = os.path.splitext(path)[0] + '.wav'
        if os.path.isfile(filename):
            return filename
        else:
            return False

    def acb_to_adx(self, path):
        offset = self.findStr(path, 'AFS2', 0, -4, 1)
        offset = self.findStr(path, '\x80\x00', offset, -2, 1)
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
