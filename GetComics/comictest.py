#!/usr/env/bin python

import unittest
import comic


class ComicTest(unittest.TestCase):
    def test_hookup(self):
        pass

    def test_find_images(self):
        comic_name = 'peanuts'

        image_paths = comic.find_images({comic_name: file('testdata/' + comic_name + '.html').read()})
        self.assertEqual(
            (comic_name, 'http://assets.amuniversal.com/87eac3e0b47e013429b4005056a9545d'),
            image_paths[comic_name])

    def test_find_dilbert_images(self):
        comic_name = 'dilbert'

        image_paths = comic.find_images({comic_name: file('testdata/' + comic_name + '.html').read()})
        self.assertEqual(('dilbert', 'http://assets.amuniversal.com/f0d6eb20b60f01342b9b005056a9545d'),
                         image_paths['dilbert'])

    def test_find_9_chick_weed_lane_images(self):
        comic_name = '9chickweedlane'

        image_paths = comic.find_images({comic_name: file('testdata/' + comic_name + '.html').read()})
        self.assertEqual(('9chickweedlane', 'http://assets.amuniversal.com/45b60cd0b5d501342b55005056a9545d'),
                         image_paths['9chickweedlane'])

    def test_find_pearls_before_swine_images(self):
        comic_name = 'pearlsbeforeswine'

        image_paths = comic.find_images({comic_name: file('testdata/' + comic_name + '.html').read()})
        self.assertEqual(
            (comic_name, 'http://assets.amuniversal.com/404fe630ba6d01343092005056a9545d'),
            image_paths[comic_name])

    def test_cannot_find_image(self):
        image_paths = comic.find_images({'dilbert': ''})
        self.assertEqual({'dilbert': ('dilbert', None)}, image_paths)
