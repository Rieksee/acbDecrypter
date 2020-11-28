# -*- coding: utf-8 -*-
import os
import sys
from src.holder.Singleton import Singleton

class EnvironmentHolder(Singleton):
    """
    docstring
    """
    projectDirectory: str

    def __init__(self):
        """
        docstring
        """
        self.projectDirectory = self.__getProjectDirectory()

    def __getProjectDirectory(self) -> str:
        if getattr(sys, 'frozen', False):
            # frozen
            return os.path.dirname(sys.executable)
        else:
            # unfrozen
            return os.path.dirname(os.path.realpath(__file__)) + "\\..\\.."
