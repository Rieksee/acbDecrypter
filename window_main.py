# -*- coding: utf-8 -*-
import os
import sys
from ui_main import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from subprocess import DEVNULL, STDOUT, check_call

class window_main(QWidget):
    def __init__(self, keyFile=None, parent=None, isolate=True):
        if not isolate:
            super(window_main, self).__init__(parent)
        else:
            super(window_main, self).__init__(None)
        self.key_default = "CF222F1FE0748978"
        self.ui = Ui_Form()
        self.keys = []
        self.note = None
        self.key = None
        self.isProcessing = True
        self.keyFile = keyFile
        self.ui.setupUi(self)
        self.setWindowTitle("HCA用鍵を選択")
        self.read_file(self.keyFile)

    def key_selected(self, index):
        self.selectedRow = index.row()
        self.note = self.keys[self.selectedRow]

    def read_file(self, file):
        if file is None:
            return
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
        QApplication.quit()

    def not_use_key(self):
        self.key = self.key_default
        self.close()
        QApplication.quit()
    
    def get_key(self):
        return self.key

    def select_file_path(self):
        path = QFileDialog.getOpenFileNames(self, "ファイルを選択", None, "ACB,AWBファイル(*.acb *acb.txt *.awb *awb.txt);;すべてのファイル(*.*)")[0]
        retval = []
        for file in path:
            retval.append(file.replace("/", "\\"))
        return retval

    def select_dir_path(self):
        path = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        path = path.replace("/", "\\")
        return path

    def command(self, attr):
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            return True
        except:
            return False
