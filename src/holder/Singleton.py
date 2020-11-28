# -*- coding: utf-8 -*-

class Singleton(object):
    __instance = None
   
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
