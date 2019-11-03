#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

from typing import List


class GridFileReader:

    def __init__(self, fn: str):
        self.fn = fn

    def read(self):
        with open(self.fn, 'r') as file:
            m = file.read()
        lines = m.splitlines()
        return [[c for c in s] for s in lines]
