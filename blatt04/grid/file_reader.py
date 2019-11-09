#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

from typing import List


def matrix_from(self, input):
    lines = input.splitlines()
    return [[c for c in s] for s in lines]


class GridFileReader:

    def __init__(self, fn: str):
        self.fn = fn

    def read(self):
        with open(self.fn, 'r') as file:
            file_content = file.read()
        return matrix_from(file_content);
