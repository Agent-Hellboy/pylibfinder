import unittest
import spotter

class SpotterTestCase(unittest.TestCase):
    def test_get_module(self):
        keyword = "eval"  # Replace with your desired keyword
        result = spotter.get_module(keyword)
        
        # Assert that the result is a list
        self.assertIsInstance(result, list)
        
        # Assert that each item in the list is a dictionary
        for item in result:
            self.assertIsInstance(item, dict)
            
            # Assert that each dictionary contains the "Module" and "Function" keys
            self.assertIn("Module", item)
            self.assertIn("Function", item)
            
            # Assert that the values of "Module" and "Function" are strings
            self.assertIsInstance(item["Module"], str)
            self.assertIsInstance(item["Function"], str)

if __name__ == "__main__":
    unittest.main()