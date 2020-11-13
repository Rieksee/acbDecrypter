# -*- coding: utf-8 -*-
import os
import sys
from ui.ui_main import Ui_Form
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtCore
from subprocess import DEVNULL, STDOUT, check_call
from PyQt5.QtWidgets import QApplication

class window_adxKeySelect(QWidget):
    def __init__(self, keyFile, parent=None, isolate=True):
        if not isolate:
            super(window_adxKeySelect, self).__init__(parent)
        else:
            super(window_adxKeySelect, self).__init__(None)
        self.key_default = "000000000000"
        self.ui = Ui_Form()
        self.keys = []
        self.note = None
        self.key = None
        self.isProcessing = True
        self.keyFile = keyFile
        self.ui.setupUi(self)
        self.setWindowTitle("ADX用鍵を選択")
        self.read_file(self.keyFile)

    def key_selected(self, index):
        self.selectedRow = index.row()
        self.note = self.keys[self.selectedRow]

    def read_file(self, file):
        with open(file, 'r', encoding='shift_jis') as f:
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
        self.key = ""
        self.close()
        QApplication.quit()

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

    def get_key(self):
        return self.key
