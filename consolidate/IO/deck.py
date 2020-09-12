# -*- coding: utf-8 -*-
import yaml
import sys
import os.path


class Deck:

    def __init__(self, inputhpath):
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath, 'r') as f:
                # Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)
        # self.type=self.doc["Problem Type"]["Type"]
