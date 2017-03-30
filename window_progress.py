# -*- coding: utf-8 -*-
import sys
from ui_progress import Ui_Progress
from PyQt5.QtWidgets import *

class window_progress(QWidget):
    def __init__(self, parent=None, isolate=True):
        if not isolate:
            super(window_progress, self).__init__(parent)
        else:
            super(window_progress, self).__init__(None)
        self.ui = Ui_Progress()
        self.ui.setupUi(self)

    def cancel(self):
        sys.exit()

    def setval(self, barNo, val):
        if type(val) != int:
            return False
        if barNo == 0:
            self.ui.progress_all.setValue(val)
        elif barNo == 1:
            self.ui.progress_now.setValue(val)
        else:
            return False
        QApplication.processEvents()
        return True
