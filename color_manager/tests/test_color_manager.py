import unittest
import json
from color_manager import Color, ColorPalette

class ColorPaletteTestCase(unittest.TestCase):
    def setUp(self):
        # Create the setup palette with grayscale colors
        palette = ColorPalette('Grayscale')
        palette.add_color('gray-100', '#f7fafc')
        palette.add_color('gray-200', '#edf2f7')
        palette.add_color('gray-300', '#e2e8f0')
        palette.add_color('gray-400', '#cbd5e0')
        palette.add_color('gray-500', '#a0aec0')
        palette.add_color('gray-600', '#718096')
        palette.add_color('gray-700', '#4a5568')
        palette.add_color('gray-800', '#2d3748')
        palette.add_color('gray-900', '#1a202c')
        self.palette = palette

    def test_to_css(self):
        css = self.palette.to_css()
        expected_css = """.gray-100 { color: #f7fafc; }
.gray-200 { color: #edf2f7; }
.gray-300 { color: #e2e8f0; }
.gray-400 { color: #cbd5e0; }
.gray-500 { color: #a0aec0; }
.gray-600 { color: #718096; }
.gray-700 { color: #4a5568; }
.gray-800 { color: #2d3748; }
.gray-900 { color: #1a202c; }
"""
        self.assertEqual(css, expected_css)

    def test_to_json(self):
        json_data = self.palette.to_json()
        expected_json = json.dumps({
            'name': 'Grayscale',
            'colors': {
                'gray-100': '#f7fafc',
                'gray-200': '#edf2f7',
                'gray-300': '#e2e8f0',
                'gray-400': '#cbd5e0',
                'gray-500': '#a0aec0',
                'gray-600': '#718096',
                'gray-700': '#4a5568',
                'gray-800': '#2d3748',
                'gray-900': '#1a202c'
            }
        })
        self.assertEqual(json_data, expected_json)

if __name__ == '__main__':
    unittest.main()
