import unittest

if __name__ == "__main__":
    unittest.defaultTestLoader.testMethodPrefix = "test"
    unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests')) 