#!/usr/env/bin python

import unittest
import comic


class ComicTest(unittest.TestCase):
    def test_hookup(self):
        pass

    def test_find_images(self):
        comic_name = 'peanuts'

        image_paths = comic.find_images({comic_name: file(comic_name + '.html').read()})
        self.assertEqual(
            (comic_name, 'http://assets.amuniversal.com/6beb10d0abb201314782005056a9545d'),
            image_paths[comic_name])

    def test_find_dilbert_images(self):
        comic_name = 'dilbert'

        image_paths = comic.find_images({comic_name: file(comic_name + '.html').read()})
        self.assertEqual(('dilbert', 'http://assets.amuniversal.com/1d879b20ec6e0132e8b6005056a9545d'),
                         image_paths['dilbert'])

    def test_find_9_chick_weed_lane_images(self):
        comic_name = '9chickweedlane'

        image_paths = comic.find_images({comic_name: file(comic_name + '.html').read()})
        self.assertEqual(('9chickweedlane', 'http://assets.amuniversal.com/e020edf0c27901315a25005056a9545d'),
                         image_paths['9chickweedlane'])

    def test_cannot_find_image(self):
        image_paths = comic.find_images({'dilbert': ''})
        self.assertEqual({'dilbert': ('dilbert', None)}, image_paths)
