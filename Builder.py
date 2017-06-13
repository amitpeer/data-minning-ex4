import pandas as pd
import re


class Builder:
    def __init__(self):
        print("Builder ctr")
        self.attributes = {}

    def build(self, path, bin):
        self.readStructure(path + "\\Structure.txt")

    def readStructure(self, path):
        print("Builder.readStructure")
        with open(path, 'r') as structure:
            for line in structure:
                lineSplitBySpaces = line.split()
                self.attributes[lineSplitBySpaces[1]] = lineSplitBySpaces[2]
