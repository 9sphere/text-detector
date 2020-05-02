# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test-text-detector
----------------------------------
Tests for `text-detector` module.
"""

import unittest

from utils.bbox import is_overlapping, is_almost_in_line, combine_boxes


class TestBboxUtils(unittest.TestCase):

    def test_bbox_is_overlapping(self):
        self.assertTrue(is_overlapping([1, 1, 3, 3], [2, 2, 4, 4]))
        self.assertTrue(is_overlapping([2, 2, 4, 4], [1, 1, 3, 3]))
        self.assertTrue(is_overlapping([2, 2, 4, 4], [2, 2, 4, 4]))
        self.assertFalse(is_overlapping([2, 2, 4, 4], [6, 2, 5, 4]))

    def test_bbox_is_almost_in_line(self):
        self.assertFalse(is_almost_in_line([1, 1, 3, 3], [2, 2, 4, 4]))
        self.assertFalse(is_almost_in_line([2, 2, 4, 4], [1, 1, 3, 3]))
        self.assertTrue(is_almost_in_line([2, 2, 4, 4], [2, 2, 4, 4]))
        self.assertFalse(is_almost_in_line([2, 2, 4, 4], [6, 2, 5, 4]))

    def test_bbox_combine_boxes(self):
        self.assertEqual([1, 1, 4, 4], combine_boxes([1, 1, 3, 3], [2, 2, 4, 4]))
        self.assertEqual([1, 1, 4, 4], combine_boxes([2, 2, 4, 4], [1, 1, 3, 3]))
        self.assertEqual([2, 2, 4, 4], combine_boxes([2, 2, 4, 4], [2, 2, 4, 4]))
        self.assertEqual([2, 2, 5, 4], combine_boxes([2, 2, 4, 4], [6, 2, 5, 4]))


if __name__ == '__main__':
    unittest.main()
