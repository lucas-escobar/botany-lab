import unittest
import lindenmayer_system as ls

class DOLSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.alphabet = {'a', 'b'}
        self.axiom = 'a'
        self.production_rules = {
            'a': 'ab',
            'b': 'a',
        }
        self.dolsystem = ls.DOLSystem(self.alphabet, self.axiom, self.production_rules)

    def test_apply_production_rules(self):
        derivation_length = 3
        expected_result = ['a', 'ab', 'aba', 'abaab']
        result = self.dolsystem.apply_production_rules(derivation_length)
        self.assertEqual(result, expected_result)

    def test_apply_production_rules_FASS(self):
        derivation_length = 1
        self.alphabet = {'Fl', 'Fr', '+', '-'}
        self.axiom = 'Fl'
        self.production_rules = {
            "Fl": "FlFl+Fr+Fr-Fl-Fl+Fr+FrFl-Fr-FlFlFr+Fl-Fr-FlFl-Fr+FlFr+Fr+Fl-Fl-FrFr+",
            "Fr": "-FlFl+Fr+Fr-Fl-FlFr-Fl+FrFr+Fl+Fr-FlFrFr+Fl+FrFl-Fl-Fr+Fr+Fl-Fl-FrFr"
        }
        self.dolsystem = ls.DOLSystem(self.alphabet, self.axiom, self.production_rules)
        expected_result = [
        'Fl', 
        'FlFl+Fr+Fr-Fl-Fl+Fr+FrFl-Fr-FlFlFr+Fl-Fr-FlFl-Fr+FlFr+Fr+Fl-Fl-FrFr+'
        ]
        result = self.dolsystem.apply_production_rules(derivation_length)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()


