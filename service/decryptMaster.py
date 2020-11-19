# -*- coding: utf-8 -*-
import os
import sys
from subprocess import DEVNULL, STDOUT, check_call
from window.window_main import window_main
from math import ceil
from PyQt5.QtWidgets import QApplication
from typing import List, Optional, Dict, Tuple

class DecryptMaster(object):
    """docstring for DecryptMaster"""
    def __init__(self, progressBar=None):
        super(DecryptMaster, self).__init__()
        if progressBar is not None:
            self.progressBar = progressBar
        self.key: Optional[str] = None
        self.progress = 0
        self.tmpDir = ""
        self.projectDir = self.get_path()
        self.errorFiles = []
        self.window_selectKey = window_main
        self.adxDecryptDir = self.projectDir + '\\adxToWav'
        self.adxSpecialDecryptPath = self.adxDecryptDir + '\\特殊鍵指定デコード.bat'
        self.adxSpecialKeyList = self.adxDecryptDir + '\\特殊鍵リスト.txt'
        self.adxDecryptPath = self.adxDecryptDir + '\\復号鍵指定デコード.bat'
        self.adxKeyList = self.adxDecryptDir + '\\復号鍵リスト.txt'
        self.afs2Dir = self.projectDir + '\\acbToHca'
        self.afs2ExePath = self.afs2Dir + '\\afs2.exe'
        self.afs2ExeCutHeadPath = self.afs2Dir + '\\先頭をカットして展開.bat'
        self.hcaDecodeDir = self.projectDir + '\\hcaToWav'
        self.hcaDecryptPath = self.hcaDecodeDir + '\\復号化.bat'
        self.hcaDecodeExePath = self.hcaDecodeDir + '\\hca.exe'
        self.hcaKeyFile = self.hcaDecodeDir + '\\復号鍵リスト.txt'
        self.keyFile = ""

    def decrypt(self, app: QApplication, path: str) -> List[str]:
        """
        override required
        """
        self.error('decrypt function is not overrided !!!')
        return list()

    def command(self, attr: List[str]) -> bool:
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except Exception as e:
            self.error(e)
            return False

    def error(self, e=None, path=None):
        if e is not None:
            print("Error: " + str(e))
        if path is not None:
            self.errorFiles.append(path)

    def get_error_files(self) -> List[str]:
        return self.errorFiles

    def get_path(self) -> str:
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__)) + "\\..\\"

    def findStr(self, file: str, searchStr: str, offset: int, back: int, count: int) -> Optional[int]:
        filesize = os.path.getsize(file)
        readLen = 40
        dataoffset: Optional[int] = None
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

    def get_progress(self) -> int:
        return self.progress

    def set_progress(self, level: int):
        self.progress = level
        if self.progressBar is not None:
            self.progressBar.setval(1, level)

    def get_filename(self, filename: str) -> Dict[int, str]:
        offset1 = self.findStr(filename, '@UTF', 0, -4, 3)
        if offset1 is None:
            return dict()
        offset2 = self.findStr(filename, 'CueName\x00CueName\x00CueIndex\x00', offset1, -len('CueName\x00CueName\x00CueIndex\x00'), 1)
        if offset2 is None:
            return dict()
        offset = offset2 + len('CueName\x00CueName\x00CueIndex\x00')
        end = self.findStr(filename, '\x00\x00', offset, -4, 1)
        if end is None:
            return dict()
        with open(filename, 'rb') as f:
            f.seek(offset)
            stri = f.read(end - offset)
            names = stri.split('\x00'.encode('ascii'))
        indexList = self.get_filename_index(filename, offset1, offset2)
        print("名前の数" + str(len(names)))
        print("indexの数" + str(len(indexList)))
        ret = {}
        count = 0
        for name in names:
            try:
                index = indexList[count]
            except Exception as e:
                index = 'unknown index:' + str(count)
            ret[index] = name.decode('utf-8')
            count = count + 1
        return ret

    def findByte(self, file: str, searchByte: bytes, offset: int, back: int, count: int) -> Optional[int]:
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

    def can_get_wav_file_name(self, nameLists: Tuple[List[str], Dict[int, str]]) -> bool:
        wavFileNames = nameLists[0]
        filenames = nameLists[1]
        if len(wavFileNames) > len(filenames):
            return False
        else:
            return True

    def get_wav_file_names(self, path: str, fileList: List[str]) -> Tuple[List[str], Dict[int, str]]:
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

        return (wavFileNames, filenames)

    def awb_file(self, path: str) -> int:
        if os.path.splitext(os.path.basename(path))[1].lower() == ".awb":
            return 1
        elif os.path.basename(path).lower().endswith("awb.txt"):
            return 2
        else:
            return 0

    def rename_wav_file(self, path: str, files_file: List[str]) -> List[str]:
        filenames = self.get_wav_file_names(path, files_file)
        if self.can_get_wav_file_name(filenames):
            newFileNames = []
            allcount = len(filenames[1])
            count = 0
            print("ファイルの数" + str(len(filenames[0])))
            for file in filenames[0]:
                try:
                    new = os.path.join(self.get_tmp_dir(), filenames[1][count] + '.wav')
                    newFileNames.append(new)
                    print(os.path.basename(file) + "--->" + os.path.basename(new))
                    self.command(['move', file, new])
                except Exception as e:
                    self.error(e)
                    newFileNames.append(file)
                # print(str(count) + "->" + os.path.basename(new))
                count = count + 1
                self.set_progress(50 + ceil(count / allcount * 25))
        else:
            newFileNames = filenames[0]
            print('wavファイル名候補数と実際のファイル数が異なっています。リネームを取りやめます。')
            self.set_progress(75)
        return newFileNames

    def get_tmp_dir(self) -> str:
        return self.tmpDir

    def select_key(self, app: QApplication, ftype: Optional[str]=None) -> str:
        if ftype is None:
            ftype = 'HCA'
        print(ftype + 'ファイルが見つかりました。鍵を選択してください。')
        self.selectKey = self.window_selectKey(self.keyFile)
        self.selectKey.show()
        app.exec_()
        key = self.selectKey.get_key()
        if key == "":
            print(ftype + "用鍵なし")
        else:
            print(ftype + "用鍵に" + key + "を使用")
        return key

    def get_filename_index(self, filename: str, offset: int, end: int) -> List[int]:
        offset2 = self.findStr(filename, '\x00\x08\x52\x00\x00\x00\x10', offset, -7, 1)
        if offset2 is None:
            return []
        offset2 = offset2 + len('\x00\x08\x52\x00\x00\x00\x10')
        with open(filename, 'rb') as f:
            f.seek(offset2)
            stri = f.read(end - offset2)
            names = stri.split('\x00\x00'.encode('ascii'))
        lineCount = 0
        result = []
        for data in names:
            if lineCount == 0:
                lineCount = lineCount + 1
                continue
            dataList = list(data)
            if len(dataList) == 0:
                try:
                   lineCount = lineCount + 1
                   continue
                except:
                   pass
            if len(dataList) < 4:
                result.append(0)
            else:
                result.append(dataList[3])
            lineCount = lineCount + 1
        return result
