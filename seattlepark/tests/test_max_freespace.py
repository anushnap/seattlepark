import unittest
import os
import pandas as pd
import numpy as np
from seattlepark import slice_df as slc
from seattlepark import max_freespace as mfs

class TestMaxFreeSpace(unittest.TestCase):

    def test_max_free_space(self):
        df = slc.slice_df('Green Lake', 'any', 12)
