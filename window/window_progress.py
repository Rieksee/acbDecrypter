# -*- coding: utf-8 -*-
import sys
import time
from ui.ui_progress import Ui_Progress
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QProgressBar
from typing import Optional, List
from src.enum.ProgressBar import ProgressBar

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

    def setval(self, barId: ProgressBar, val: int) -> bool:
        if type(val) != int:
            return False
        bar = self.getBar(barId)
        if bar is None:
            return False
        bar.setValue(val)
        QApplication.processEvents()
        return True

    def getVal(self, barId: ProgressBar) -> Optional[int]:
        bar = self.getBar(barId)
        if bar is None:
            return None
        return bar.value()

    def finish(self):
        QApplication.quit()

    def select_file_path(self) -> List[str]:
        path = QFileDialog.getOpenFileNames(self, "ファイルを選択", None, "ACB,AWBファイル(*.acb *acb.txt *.awb *awb.txt);;すべてのファイル(*.*)")[0]
        retval: List[str] = []
        for file in path:
            retval.append(file.replace("/", "\\"))
        return retval

    def select_dir_path(self) -> str:
        path = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        path = path.replace("/", "\\")
        return path

    def getBar(self, barId: ProgressBar) -> Optional[QProgressBar]:
        if barId == ProgressBar.ALL:
            return self.ui.progress_all
        elif barId == ProgressBar.CURRENT:
            return self.ui.progress_now
        else:
            return None
