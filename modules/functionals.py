import os

class OptionalKwargs():
    def __init__(self,kwargs):
        self.dictionary = kwargs

    def __getitem__(self,key)->str:
        if key in self.dictionary.keys():
            return self.dictionary[key]
        return None
