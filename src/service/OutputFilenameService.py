# -*- coding: utf-8 -*-
import os
from typing import Dict, List, Tuple
from src.component.FileAnalyzeComponent import FileAnalyzeComponent
from src.component.OutputFilenameComponent import OutputFilenameComponent

class OutputFilenameService(object):
    """
    docstring
    """
    @staticmethod
    def get_filename(filename: str) -> Dict[int, str]:
        offset1 = FileAnalyzeComponent.findStr(filename, '@UTF', 0, -4, 3)
        if offset1 is None:
            return dict()
        offset2 = FileAnalyzeComponent.findStr(filename, 'CueName\x00CueName\x00CueIndex\x00', offset1, -len('CueName\x00CueName\x00CueIndex\x00'), 1)
        if offset2 is None:
            return dict()
        offset = offset2 + len('CueName\x00CueName\x00CueIndex\x00')
        end = FileAnalyzeComponent.findStr(filename, '\x00\x00', offset, -4, 1)
        if end is None:
            return dict()
        with open(filename, 'rb') as f:
            f.seek(offset)
            stri = f.read(end - offset)
            names = stri.split('\x00'.encode('ascii'))
        indexList = FileAnalyzeComponent.get_filename_index(filename, offset1, offset2)
        print("名前の数" + str(len(names)))
        print("indexの数" + str(len(indexList)))
        ret = {}
        count = 0
        for name in names:
            try:
                index = indexList[count]
            except Exception as e:
                index = 'unknown index:' + str(count)
            ret[index] = name.decode('utf-8')
            count = count + 1
        return ret

    @staticmethod
    def get_wav_file_names(path: str, fileList: List[str]) -> Tuple[List[str], Dict[int, str]]:
        # 連番の名前
        wavFileNames = [os.path.splitext(file)[0] + '.wav' for file in fileList]

        # acbファイルに格納されている元の名前
        filenames = OutputFilenameService.get_filename(path)

        # 調査したのがawbファイルで元ファイル名が見つからない場合acbファイルも調査する
        if len(filenames) == 0 and OutputFilenameComponent.awb_file(path) != 0:
            if OutputFilenameComponent.awb_file(path) == 1:
                filenames = OutputFilenameService.get_filename(os.path.splitext(path)[0] + ".acb")
            elif OutputFilenameComponent.awb_file(path) == 2:
                acbpath = path[:len(path) - len('awb.txt')] + 'acb.txt'
                filenames = OutputFilenameService.get_filename(acbpath)

        return (wavFileNames, filenames)
