# -*- coding:utf-8 -*-
import sys
import os
from subprocess import DEVNULL, STDOUT, check_call
from PyQt5.QtWidgets import QApplication
from window.window_progress import window_progress
from service.dec import Decrypt
from typing import List

class AcbDecrypter(object):
    """
    docstring
    """
    def main(self, path: List[str], folder: bool) -> None:
        app = QApplication([sys.argv[0]])
        self.window_progress = window_progress()
        if folder:
            self.folder = self.window_progress.select_dir_path()
            if self.folder == "":
                sys.exit()
            self.path = self.find_acb_files([self.folder])
        else:
            self.folder = None
            if len(path) == 0:
                self.path = self.window_progress.select_file_path()
            else:
                self.path = path
        if len(self.path) == 0:
            print("処理対象のファイルが見つかりません。")
            sys.exit()
        self.key_default = "CF222F1FE0748978"
        self.custumFolder = folder
        self.note = None
        self.key = None
        if not self.isEncrypted():
            self.key = self.key_default
            sys.exit()
        self.window_progress.show()
        self.decrypt = Decrypt(app, self.window_progress, self.path, self.folder)
        sys.exit()
        # sys.exit(app.exec_())

    def get_path(self) -> str:
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

    def isEncrypted(self) -> bool:
        offset = None
        data = self.open_hca()
        for no, bt in enumerate(data):
            if bt == 99 or bt == 227:
                if self.byte_chk(bt, no, data):
                    offset = no
                    break
        if offset is None:
            return True
        if data[offset + 5] == 1 or data[offset + 5] == 0:
            return False
        else:
            return True

    def open_hca(self):
        thisFileDir = self.get_path()
        afs2Dir = thisFileDir + '\\acbToHca'
        afs2ExeCutHeadPath = afs2Dir + '\\先頭をカットして展開.bat'
        self.command([afs2ExeCutHeadPath, self.path[0]])
        folderName = os.path.splitext(os.path.basename(self.path[0]))[0]
        hcasDir = afs2Dir + '\\' + folderName
        try:
            file = os.listdir(hcasDir)
        except:
            return []
        filePath = os.path.join(hcasDir, file[0])
        if not os.path.isfile(filePath):
            return []
        with open(filePath, 'rb') as f:
            f.seek(20)
            data = f.read(60)
        data = bytearray(data)
        self.command(['rd', '/s', '/q', hcasDir])
        return data

    def byte_chk(self, ty: int, index: int, data) -> bool:
        if ty == 99:
            chk = [105, 112, 104]
        elif ty == 227:
            chk = [233, 240, 232]
        for ch in chk:
            index = index + 1
            try:
                if data[index] != ch:
                    return False
            except:
                return False
        return True

    def find_acb_files(self, directories: List[str]) -> List[str]:
        ret = []
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1] in [".acb", ".awb"] or file.lower().endswith("acb.txt") or file.lower().endswith("awb.txt"):
                        ret.append(os.path.join(root, file))
                ret.extend(self.find_acb_files(dirs))
        return ret

    def command(self, attr: List[str]) -> bool:
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except:
            return False

    def finish_decrypt(self):
        sys.exit()

if __name__ == '__main__':
    print("このツールはID: f70CrkXN さんの\nAFS2(.awb)CPK(.cpk)展開ツール v1.40 と\nHCAデコーダ v1.20 の機能をラップしたものです。\n基幹機能は f70CrkXN さんによるものですので感謝を...\n\n")
    folder = False
    if len(sys.argv) > 1:
        path = []
        flag = 0
        for arg in sys.argv:
            if flag != 1:
                flag = 1
                continue
            path.append(arg)
    else:
        ans = input("フォルダを選択？[y/N]>>")
        if ans.lower() == "y":
            folder = True
        path = []
    AcbDecrypter().main(path, folder)
