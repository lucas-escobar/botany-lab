import unittest
import lindenmayer_system as ls

class ImageProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.width = 400 
        self.height = 400 
        self.output_file = './test.jpg'
        self.bg_color = (233,234,239) # 
        self.image_processor= ls.ImageProcessor(
            self.width,
            self.height,
            self.output_file,
            self.bg_color
        )

    def test_draw_line(self):
        p1 = (self.width / 2, self.height / 2)
        p2 = (self.width / 3, self.height / 3)
        width = 1
        color = (75,106,136)
        self.image_processor.draw_line(p1[0], p1[1], p2[0], p2[1], color, width)
        # checks pixel values at each endpoint of the image
        # this could use some improvement
        pixels = self.image_processor.image.load()
        self.assertEqual(pixels[p1[0], p1[1]], color)
        self.assertEqual(pixels[p2[0], p2[1]], color)


if __name__ == "__main__":
    unittest.main()
