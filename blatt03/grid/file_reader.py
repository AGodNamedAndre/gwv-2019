#!/usr/bin/env python3
import numpy as np
from typing import List


class GridFileReader:

    def __init__(self, fn: str):
        self.fn = fn

    def read(self):
        with open(self.fn) as file:
            lines: List[str] = file.read().splitlines()

        for l in lines:
            print(l)

        na = np.asarray(lines)
        print(na)
        print(na[0][0])
