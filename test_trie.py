#!/usr/bin/env python3
"""Tests for the Trie implementation."""

import unittest
import tempfile
import os
from trie import Trie


class TestTrie(unittest.TestCase):
    """Test cases for Trie data structure."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.trie = Trie()
    
    def test_insert_and_search(self):
        """Test basic insert and search operations."""
        words = ['cat', 'car', 'card', 'care', 'careful', 'cats', 'dog']
        
        for word in words:
            self.trie.insert(word)
        
        # Test existing words
        for word in words:
            self.assertTrue(self.trie.search(word), f"Word '{word}' should be found")
        
        # Test non-existing words
        non_words = ['ca', 'card.', 'caring', 'dogs', 'zebra']
        for word in non_words:
            self.assertFalse(self.trie.search(word), f"Word '{word}' should not be found")
    
    def test_starts_with(self):
        """Test prefix checking."""
        words = ['cat', 'car', 'card', 'care', 'careful']
        
        for word in words:
            self.trie.insert(word)
        
        # Test valid prefixes
        self.assertTrue(self.trie.starts_with('c'))
        self.assertTrue(self.trie.starts_with('ca'))
        self.assertTrue(self.trie.starts_with('car'))
        self.assertTrue(self.trie.starts_with('care'))
        
        # Test invalid prefixes
        self.assertFalse(self.trie.starts_with('d'))
        self.assertFalse(self.trie.starts_with('cart'))
        self.assertFalse(self.trie.starts_with('careless'))
    
    def test_case_insensitive(self):
        """Test case insensitive operations."""
        self.trie.insert('CaT')
        
        self.assertTrue(self.trie.search('cat'))
        self.assertTrue(self.trie.search('CAT'))
        self.assertTrue(self.trie.search('Cat'))
        self.assertTrue(self.trie.starts_with('ca'))
        self.assertTrue(self.trie.starts_with('CA'))
    
    def test_empty_and_none_inputs(self):
        """Test handling of empty and None inputs."""
        self.assertFalse(self.trie.search(''))
        self.assertFalse(self.trie.search(None))
        self.assertTrue(self.trie.starts_with(''))
        self.assertTrue(self.trie.starts_with(None))
    
    def test_load_from_file(self):
        """Test loading words from a file."""
        # Create temporary dictionary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_words = ['apple\n', 'banana\n', 'cherry\n', 'dog\n', 'elephant\n']
            f.writelines(test_words)
            temp_file = f.name
        
        try:
            count = self.trie.load_from_file(temp_file)
            self.assertEqual(count, 5)
            
            # Test that words were loaded correctly
            self.assertTrue(self.trie.search('apple'))
            self.assertTrue(self.trie.search('banana'))
            self.assertTrue(self.trie.search('cherry'))
            self.assertTrue(self.trie.search('dog'))
            self.assertTrue(self.trie.search('elephant'))
            
        finally:
            os.unlink(temp_file)
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file."""
        count = self.trie.load_from_file('/nonexistent/file.txt')
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()