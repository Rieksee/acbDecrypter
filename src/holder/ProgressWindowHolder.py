# -*- coding: utf-8 -*-
from src.holder.Singleton import Singleton
from window.window_progress import window_progress
from src.enum.ProgressBar import ProgressBar

class ProgressWindowHolder(Singleton):
    """
    docstring
    """
    __window: window_progress

    def setWindow(self, window: window_progress):
        self.__window = window

    def getWindow(self):
        return self.__window

    def setProgress(self, barId: ProgressBar, level: int):
        """
        set progress by given barId
        """
        self.__window.setval(barId=barId, val=level)

    def getProgress(self, barId: ProgressBar) -> int:
        """
        get progress by given barId
        """
        return self.__window.getVal(barId)
