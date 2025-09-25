#!/usr/bin/env python3
"""Integration tests for the Letter Boxed solver."""

import unittest
import tempfile
import os
from solver import LetterBoxSolver


class TestLetterBoxSolverIntegration(unittest.TestCase):
    """Integration tests for the complete Letter Boxed solver."""
    
    def setUp(self):
        """Set up test fixtures with a small dictionary."""
        # Create a small test dictionary
        test_words = [
            'cat', 'dog', 'bat', 'hat', 'car', 'tar', 'art', 'rat',
            'ace', 'ice', 'age', 'cage', 'rage', 'face', 'race',
            'bad', 'dad', 'sad', 'had', 'mad', 'bag', 'tag', 'rag',
            'bed', 'red', 'fed', 'led', 'wed', 'beg', 'leg', 'peg'
        ]
        
        # Create temporary dictionary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        for word in test_words:
            self.temp_file.write(word + '\n')
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_file.name)
    
    def test_solver_initialization(self):
        """Test solver initializes correctly."""
        solver = LetterBoxSolver(['AB', 'CD', 'EF', 'GH'], self.temp_file.name)
        
        # Check ATM is initialized
        self.assertEqual(solver.atm.all_letters, {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'})
        
        # Check trie has words
        self.assertTrue(solver.trie.search('cat'))
        self.assertTrue(solver.trie.search('dog'))
        self.assertFalse(solver.trie.search('xyz'))
    
    def test_find_words_starting_with(self):
        """Test finding words that start with a specific letter."""
        solver = LetterBoxSolver(['AB', 'CD', 'EF', 'GH'], self.temp_file.name)
        
        # Find words starting with 'C'
        words = solver.find_words_starting_with('C')
        
        # Should find words that are valid according to ATM rules
        valid_words = []
        for word in words:
            if solver.atm.is_valid_word(word):
                valid_words.append(word)
        
        # Should have some valid words
        self.assertGreater(len(valid_words), 0)
    
    def test_simple_puzzle_solving(self):
        """Test solving a simple puzzle."""
        # Use a configuration that should have solutions
        solver = LetterBoxSolver(['CAR', 'BDG', 'ETH', 'FIL'], self.temp_file.name)
        
        # Try to find solutions
        solutions = solver.solve(max_words=3, min_word_length=3)
        
        # Verify solutions structure
        for solution in solutions[:5]:  # Check first 5 solutions
            self.assertIsInstance(solution, list)
            self.assertGreater(len(solution), 0)
            
            # Each word in solution should be valid
            for word in solution:
                self.assertIsInstance(word, str)
                self.assertGreater(len(word), 0)
                self.assertTrue(solver.trie.search(word))
                self.assertTrue(solver.atm.is_valid_word(word))
    
    def test_word_chaining(self):
        """Test that words in solutions are properly chained."""
        solver = LetterBoxSolver(['AB', 'CD', 'EF', 'GH'], self.temp_file.name)
        
        # Find a few words for testing
        words_a = solver.find_words_starting_with('A')[:5]
        
        for word in words_a:
            if len(word) > 0:
                last_letter = word[-1].upper()
                next_words = solver.find_words_starting_with(last_letter)[:3]
                
                # If there are next words, verify they start with the last letter
                for next_word in next_words:
                    if next_word:
                        self.assertEqual(next_word[0].upper(), last_letter)
    
    def test_atm_constraints(self):
        """Test that ATM constraints are properly enforced."""
        solver = LetterBoxSolver(['AB', 'CD', 'EF', 'GH'], self.temp_file.name)
        
        # Test that invalid transitions are rejected
        self.assertFalse(solver.atm.is_valid_word('AB'))  # Same side
        self.assertFalse(solver.atm.is_valid_word('CD'))  # Same side
        
        # Test that valid transitions are accepted
        self.assertTrue(solver.atm.is_valid_word('AC'))   # Different sides
        self.assertTrue(solver.atm.is_valid_word('AE'))   # Different sides


if __name__ == '__main__':
    unittest.main()