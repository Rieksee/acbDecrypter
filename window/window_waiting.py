# -*- coding: utf-8 -*-
import os
import sys
from ui.ui_waiting import Ui_Dialog
from subprocess import DEVNULL, STDOUT, check_call
from PyQt5.QtWidgets import QApplication, QWidget
from typing import List

class window_waiting(QWidget):
    def __init__(self, parent=None, isolate=True):
        if not isolate:
            super(window_waiting, self).__init__(parent)
        else:
            super(window_waiting, self).__init__(None)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def command(self, attr: List[str]) -> bool:
        try:
            check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
            self.close()
            QApplication.quit()
            return True
        except Exception as e:
            self.error(e)
            self.close()
            QApplication.quit()
            return False

    def error(self, e: Exception=None):
        if e is not None:
            print("Error: " + str(e))
