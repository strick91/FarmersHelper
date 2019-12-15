import unittest
from Dictionaries import *
import sys
import io


class MyTestCase(unittest.TestCase):
    def test_function(self):
        prices_contents = [['beef', 'ribeye', '12'], ['beef', 'newyork', '14'], ['beef', 'burger', '6'], ['beef', 'tbone', '12'], ['pork', 'porkchops', '7.5'], ['chicken', 'whole', '3.5'], ['pork', 'hamsteak', '6.5'], ['chicken', 'eggs', '3.25']]
        inventory_contents = [['beef', 'newyork', '2.88'], ['beef', 'ribeye', '2.27'], ['beef', 'ribeye', '2.42'], ['beef', 'tbone', '2.13'], ['beef', 'burger', '285'], ['pork', 'porkchops', '2.03'], ['pork', 'porkchops', '2.18'], ['pork', 'hamsteak', '1.25'], ['chicken', 'whole', '5.5'], ['chicken', 'eggs', '25']]
        dictionaries = CategoryDicts(prices_contents, inventory_contents)
        inventory_output_all = io.StringIO()
        sys.stdout = inventory_output_all
        dictionaries.DisplayInventory("all")
        test1 = r"""beef: {'newyork': ['2.88'], 'ribeye': ['2.27', '2.42'], 'tbone': ['2.13'], 'burger': ['285']}
Category worth: $1832.16 
pork: {'porkchops': ['2.03', '2.18'], 'hamsteak': ['1.25']}
Category worth: $39.7 
chicken: {'whole': ['5.5'], 'eggs': ['25']}
Category worth: $100.5 
Total inventory worth: $1972.36"""
        self.assertEqual(inventory_output_all.getvalue().split(), test1.split())

        test2 = r"""beef: {'newyork': ['2.88'], 'ribeye': ['2.27', '2.42'], 'tbone': ['2.13'], 'burger': ['285']}
Category worth: $1832.16"""
        inventory_output_beef = io.StringIO()
        sys.stdout = inventory_output_beef
        dictionaries.DisplayInventory("beef")
        self.assertEqual(inventory_output_beef.getvalue().split(), test2.split())

        test3 = r"""pork: {'porkchops': ['2.03', '2.18'], 'hamsteak': ['1.25']}
Category worth: $39.7"""
        inventory_output_pork = io.StringIO()
        sys.stdout = inventory_output_pork
        dictionaries.DisplayInventory("pork")
        self.assertEqual(inventory_output_pork.getvalue().split(), test3.split())

        test4 = r"""chicken: {'whole': ['5.5'], 'eggs': ['25']}
Category worth: $100.5"""
        inventory_output_chicken = io.StringIO()
        sys.stdout = inventory_output_chicken
        dictionaries.DisplayInventory("chicken")
        self.assertEqual(inventory_output_chicken.getvalue().split(), test4.split())


if __name__ == '__main__':
    unittest.main()
