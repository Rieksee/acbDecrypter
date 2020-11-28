# -*- coding: utf-8 -*-
from typing import List
from subprocess import DEVNULL, STDOUT, check_call

class CommandExecuterComponent(object):
    """
    docstring
    """
    @staticmethod
    def command(attr: List[str]) -> bool:
        check_call(attr, shell=True, stdout=DEVNULL, stderr=STDOUT)
        return True
