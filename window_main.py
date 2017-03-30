# -*- coding: utf-8 -*-
import os
import sys
from ui_main import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from dec import Decrypt
from subprocess import DEVNULL, STDOUT, check_call

class window_main(QWidget):
    def __init__(self, path, keyFile, folder=False, parent=None, isolate=True):
        if not isolate:
            super(window_main, self).__init__(parent)
        else:
            super(window_main, self).__init__(None)
        if folder:
            self.folder = self.select_dir_path()
            if self.folder == "":
                sys.exit()
            self.path = self.find_acb_files([self.folder])
        else:
            self.folder = None
            if len(path) == 0:
                self.path = self.select_file_path()
            else:
                self.path = path
        if len(self.path) == 0:
            print("処理対象のファイルが見つかりません。")
            sys.exit()
        self.key_default = "CF222F1FE0748978"
        self.custumFolder = folder
        self.ui = Ui_Form()
        self.keys = []
        self.note = None
        self.key = None
        self.keyFile = keyFile
        if not self.isEncrypted():
            self.not_use_key()
            sys.exit()
        self.ui.setupUi(self)
        self.read_file(self.keyFile)

    def key_selected(self, index):
        self.selectedRow = index.row()
        self.note = self.keys[self.selectedRow]

    def read_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                lis = line.split(' : ')
                if len(lis) != 2:
                    continue
                key = (lis[1], lis[0])
                self.keys.append(key)
        self.ui.model = QtGui.QStandardItemModel(self.ui.listView)
        for key in self.keys:
            item = QtGui.QStandardItem(key[0].rstrip('\n'))
            self.ui.model.appendRow(item)
        self.ui.listView.setModel(self.ui.model)

    def enter(self):
        if self.note is None:
            msg = QMessageBox()
            message = "デフォルト鍵を使用します。"
            msg = msg.information(self, 'info', message,  QMessageBox.Ok, QMessageBox.Ok)
            if msg != QMessageBox.Ok:
                return
            self.key = self.key_default
        else:
            self.key = self.note[1]
        self.close()
        Decrypt(self.path, self.key, self.folder)

    def not_use_key(self):
        self.key = self.key_default
        self.close()
        Decrypt(self.path, self.key, self.folder)

    def select_file_path(self):
        path = QFileDialog.getOpenFileNames(self, "ファイルを選択", None, "ACBファイル(*.acb *.acb.txt)")[0]
        retval = []
        for file in path:
            retval.append(file.replace("/", "\\"))
        return retval

    def select_dir_path(self):
        path = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        path = path.replace("/", "\\")
        return path

    def find_acb_files(self, directories):
        ret = []
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1] == ".acb" or file.endswith(".acb.txt"):
                        ret.append(os.path.join(root, file))
                ret.extend(self.find_acb_files(dirs))
        return ret

    def isEncrypted(self):
        offset = 0
        data = self.open_hca()
        for no, bt in enumerate(data):
            if bt == 99 or bt == 227:
                if self.byte_chk(bt, no, data):
                    offset = no
                    break
        if data[offset + 5] == 1 or data[offset + 5] == 0:
            return False
        else:
            return True

    def byte_chk(self, ty, index, data):
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

    def get_path(self):
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__))

    def command(self, attr):
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except:
            return False
