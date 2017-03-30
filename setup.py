# -*- coding: utf-8 -*-
import sys
import os
from cx_Freeze import setup, Executable

base = None

#コンソールアプリの場合は↓この行コメントアウト or 削除すること
# if sys.platform == 'win32' : 
# base = 'Win32GUI'

# exe にしたい python ファイルを指定
exe = Executable(
	script='acbDecrypter.py',
	base=base,
	)

excludes = ['unittest', 'email', 'urllib', 'xml', 'logging', 'http', 'html']

# セットアップ
setup(name = 'acbDecrypter',
    version = '0.1.1',
    options = {'build_exe': {'excludes':excludes}},
    description = 'test',
    executables = [exe])
