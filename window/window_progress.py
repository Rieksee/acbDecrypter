# -*- coding: utf-8 -*-
import sys
from ui.ui_progress import Ui_Progress
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

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

    def setval(self, barNo: int, val: int):
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

    def finish(self):
        QApplication.quit()

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
