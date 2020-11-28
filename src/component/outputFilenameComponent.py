# -*- coding: utf-8 -*-
import os
from typing import Tuple, List, Dict
from src.component.FileAnalyzeComponent import FileAnalyzeComponent

class OutputFilenameComponent(object):
    """
    docstring
    """
    @staticmethod
    def can_get_wav_file_name(nameLists: Tuple[List[str], Dict[int, str]]) -> bool:
        wavFileNames = nameLists[0]
        filenames = nameLists[1]
        if len(wavFileNames) > len(filenames):
            return False
        else:
            return True

    @staticmethod
    def awb_file(path: str) -> int:
        if os.path.splitext(os.path.basename(path))[1].lower() == ".awb":
            return 1
        elif os.path.basename(path).lower().endswith("awb.txt"):
            return 2
        else:
            return 0
