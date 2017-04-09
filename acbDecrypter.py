# -*- coding:utf-8 -*-
import sys
import os
from preWorksForDecrypt import pre_works_for_decrypt

def get_path():
    if getattr(sys, 'frozen', False):
        # frozen
        return os.path.dirname(sys.executable)
    else:
        # unfrozen
        return os.path.dirname(os.path.realpath(__file__))

def main(path, folder):
    pre_works_for_decrypt(path, folder)


if __name__ == '__main__':
    print("このツールはID: f70CrkXN さんの\nAFS2(.awb)CPK(.cpk)展開ツール v1.40 と\nHCAデコーダ v1.20 の機能をラップしたものです。\n基幹機能は f70CrkXN さんによるものですので感謝を...\n\n")
    folder = False
    if len(sys.argv) > 1:
        path = []
        flag = 0
        for arg in sys.argv:
            if flag != 1:
                flag = 1
                continue
            path.append(arg)
    else:
        ans = input("フォルダを選択？[y/N]>>")
        if ans.lower() == "y":
            folder = True
        path = []
    main(path, folder)
