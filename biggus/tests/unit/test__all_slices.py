# (C) British Crown Copyright 2014, Met Office
#
# This file is part of Biggus.
#
# Biggus is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Biggus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Biggus. If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for `biggus._all_slices`."""

from contextlib import contextmanager
import unittest

import numpy as np

import biggus
from biggus import _all_slices, _all_slices_inner
from biggus.tests import mock


class Test__all_slices(unittest.TestCase):
    @contextmanager
    def set_chunk_size(self, value):
        old_chunk_size = biggus.MAX_CHUNK_SIZE
        biggus.MAX_CHUNK_SIZE = value
        yield
        biggus.MAX_CHUNK_SIZE = old_chunk_size

    def test_all_cases(self):
        array = biggus.ConstantArray((4, 3, 5), dtype=np.float32)
        # Chunk size set to fit in two items from the second dimension into a
        # single chunk, but not the whole dimension.
        chunk_size = (32 / 8) * 5 * 3 - 1
        with self.set_chunk_size(chunk_size):
            slices = _all_slices(array)
        expected = [[0, 1, 2, 3],
                    [slice(0, 2, None), slice(2, 3, None)],
                    (slice(None, None, None),)]
        self.assertEqual(slices, expected)

    def test_always_slices(self):
        array = biggus.ConstantArray((3, 5), dtype=np.float32)
        chunk_size = (32 / 8) * 5 - 1
        with self.set_chunk_size(chunk_size):
            slices = _all_slices_inner(array.dtype.itemsize, array.shape,
                                       always_slices=True)
        expected = [[slice(0, 1, None), slice(1, 2, None), slice(2, 3, None)],
                    [slice(0, 4, None), slice(4, 5, None)]]
        self.assertEqual(slices, expected)


if __name__ == '__main__':
    unittest.main()
