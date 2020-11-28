# -*- coding: utf-8 -*-
import os
import sys
from subprocess import DEVNULL, STDOUT, check_call
from window.window_main import window_main
from window.window_progress import window_progress
from math import ceil
from PyQt5.QtWidgets import QApplication
from typing import List, Optional, Dict, Tuple
from src.component.FileAnalyzeComponent import FileAnalyzeComponent
from src.component.OutputFilenameComponent import OutputFilenameComponent
from src.component.CommandExecuterComponent import CommandExecuterComponent
from src.holder.EnvironmentHolder import EnvironmentHolder
from src.service.OutputFilenameService import OutputFilenameService
from src.holder.ProgressWindowHolder import ProgressWindowHolder
from src.enum.ProgressBar import ProgressBar

class DecryptMaster(object):
    """docstring for DecryptMaster"""
    def __init__(self):
        super(DecryptMaster, self).__init__()
        self.key: Optional[str] = None
        self.progress = 0
        self.tmpDir = ""
        self.projectDir = self.get_path()
        self.errorFiles: List[str] = []
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
            return CommandExecuterComponent.command(attr)
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
        return EnvironmentHolder().projectDirectory

    def findStr(self, file: str, searchStr: str, offset: int, back: int, count: int) -> Optional[int]:
        return FileAnalyzeComponent.findStr(file=file, searchStr=searchStr, offset=offset, back=back, count=count)

    def get_progress(self) -> int:
        return ProgressWindowHolder().getProgress(ProgressBar.CURRENT)

    def set_progress(self, level: int):
        ProgressWindowHolder().setProgress(ProgressBar.CURRENT, level)

    def get_filename(self, filename: str) -> Dict[int, str]:
        return OutputFilenameService.get_filename(filename=filename)

    def findByte(self, file: str, searchByte: bytes, offset: int, back: int, count: int) -> Optional[int]:
        return FileAnalyzeComponent.findByte(file=file, searchByte=searchByte, offset=offset, back=back, count=count)

    def can_get_wav_file_name(self, nameLists: Tuple[List[str], Dict[int, str]]) -> bool:
        return OutputFilenameComponent.can_get_wav_file_name(nameLists=nameLists)

    def get_wav_file_names(self, path: str, fileList: List[str]) -> Tuple[List[str], Dict[int, str]]:
        return OutputFilenameService.get_wav_file_names(path=path, fileList=fileList)

    def awb_file(self, path: str) -> int:
        return OutputFilenameComponent.awb_file(path=path)

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
        return FileAnalyzeComponent.get_filename_index(filename=filename, offset=offset, end=end)
