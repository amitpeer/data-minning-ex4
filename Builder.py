import pandas as pd
import re
class Builder:

    def __init__(self):
        print("Builder ctr")



    def readStructure(self, path):
        file = open(path, 'r')
        