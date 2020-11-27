# -*- coding: utf-8 -*-
import os
from typing import Optional, Dict, List

class FileAnalyzeComponent(object):
    """
    This is a component for analyzing files
    """
    @staticmethod
    def findStr(file: str, searchStr: str, offset: int, back: int, count: int) -> Optional[int]:
        filesize = os.path.getsize(file)
        readLen = 40
        dataoffset: Optional[int] = None
        with open(file, 'rb') as f:
            while True:
                f.seek(offset)
                data = f.read(readLen)
                findAt = data.find(searchStr.encode('utf-8'))
                if findAt != -1:
                    dataoffset = findAt + offset
                    count = count - 1
                    if count <= 0:
                        break
                if offset + readLen > filesize:
                    dataoffset = None
                    break
                offset = offset + readLen + back
            return dataoffset

    @staticmethod
    def findByte(file: str, searchByte: bytes, offset: int, back: int, count: int) -> Optional[int]:
        filesize = os.path.getsize(file)
        readLen = 40
        search = None
        searchArray = bytearray(searchByte)
        with open(file, 'rb') as f:
            while True:
                f.seek(offset)
                data = f.read(readLen)
                matchCount = 0
                data = bytearray(data)
                dataCount = 0
                for bt in data:
                    if bt == searchArray[matchCount]:
                        # 一致したとき
                        if matchCount == 0:
                            findAt = dataCount
                        matchCount = matchCount + 1
                    else:
                        # 一致しない時
                        matchCount = 0
                    dataCount = dataCount + 1
                    if matchCount >= len(searchArray):
                        break
                else:
                    # 一致しないままreadしたdataを読み終わったとき
                    if offset + readLen > filesize:
                        # ファイルの最後まで読んでいるとき
                        dataoffset = None
                        break
                    offset = offset + readLen + back
                    continue
                dataoffset = findAt + offset
                count = count - 1
                if count <= 0:
                    break
            return dataoffset

    @staticmethod
    def get_filename_index(filename: str, offset: int, end: int) -> List[int]:
        offset2 = FileAnalyzeComponent.findStr(filename, '\x00\x08\x52\x00\x00\x00\x10', offset, -7, 1)
        if offset2 is None:
            return []
        offset2 = offset2 + len('\x00\x08\x52\x00\x00\x00\x10')
        with open(filename, 'rb') as f:
            f.seek(offset2)
            stri = f.read(end - offset2)
            names = stri.split('\x00\x00'.encode('ascii'))
        lineCount = 0
        result = []
        for data in names:
            if lineCount == 0:
                lineCount = lineCount + 1
                continue
            dataList = list(data)
            if len(dataList) == 0:
                try:
                   lineCount = lineCount + 1
                   continue
                except:
                   pass
            if len(dataList) < 4:
                result.append(0)
            else:
                result.append(dataList[3])
            lineCount = lineCount + 1
        return result
