import glob
import cv2
import sys
import unittest

sys.path.insert(1, "../")
sys.path.insert(1, "../modules")

from modules.hw_detector import *


# =====================================================================================================================
class MyTestCases(unittest.TestCase):

    def test_one_image(self):

        config = Config('../cfg/config.yml')

        # No need to draw or trace in Unit test
        config.trace = False
        config.gui = False

        template = cv2.imread('../dataset/templates/' + config.puncture_tpl_file + '.jpg')

        self.assertEqual(template.size > 0, True)

        fname = 'MwPic_30_1_2015__16_1__29_407.JPG'

        self.assertEqual(len(fname) > 0, True)

        img = cv2.imread('../dataset/' + fname)

        self.assertEqual(img.size > 0, True)

        final, d1, d2, hw = hw_detector(img, fname, template, config)

        self.assertEqual(d1 > 0, True)
        self.assertEqual(d2 > 0, True)
        self.assertEqual(hw > 0, True)
        self.assertEqual(final.size > 0, True)

# =====================================================================================================================


# =====================================================================================================================
if __name__ == '__main__':
    unittest.main()
# =====================================================================================================================