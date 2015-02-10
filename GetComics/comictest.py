#!/usr/env/bin python

import unittest

import comic

class ComicTest(unittest.TestCase):
    def testHookup(self):
        pass

    def testFindImages(self):
        comic_name = 'peanuts'

        imagePaths = comic.FindImages({comic_name:file(comic_name +'.html').read()})
        self.assertEqual((comic_name, 'http://assets.amuniversal.com/6beb10d0abb201314782005056a9545d'), imagePaths[comic_name])

    def testFindDilbertImages(self):
        comic_name = 'dilbert'

        imagePaths = comic.FindImages({comic_name:file(comic_name +'.html').read()})
        self.assertEqual(('dilbert', 'http://assets.amuniversal.com/ae6d983070e40132b90b005056a9545d'),
                         imagePaths['dilbert'])

    def testFind9ChickWeedLaneImages(self):
        comic_name = '9chickweedlane'

        imagePaths = comic.FindImages({comic_name:file(comic_name +'.html').read()})
        self.assertEqual(('9chickweedlane', 'http://assets.amuniversal.com/e020edf0c27901315a25005056a9545d'),
                         imagePaths['9chickweedlane'])

    def testCannotFindImage(self):
        imagePaths = comic.FindImages({'dilbert':''})
        self.assertEqual({'dilbert': ('dilbert', None)}, imagePaths)

        
