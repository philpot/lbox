#!/usr/bin/env python3
"""Tests for the LetterBoxATM implementation."""

import unittest
from letterbox_atm import LetterBoxATM


class TestLetterBoxATM(unittest.TestCase):
    """Test cases for Letter Box ATM."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Standard test configuration
        self.atm = LetterBoxATM(['ABC', 'DEF', 'GHI', 'JKL'])
    
    def test_initialization(self):
        """Test ATM initialization."""
        expected_letters = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'}
        self.assertEqual(self.atm.all_letters, expected_letters)
        
        # Test letter to side mapping
        self.assertEqual(self.atm.letter_to_side['A'], 0)
        self.assertEqual(self.atm.letter_to_side['D'], 1)
        self.assertEqual(self.atm.letter_to_side['G'], 2)
        self.assertEqual(self.atm.letter_to_side['J'], 3)
    
    def test_valid_transitions(self):
        """Test valid transition checking."""
        # Valid transitions (different sides)
        self.assertTrue(self.atm.is_valid_transition('A', 'D'))  # Side 0 to 1
        self.assertTrue(self.atm.is_valid_transition('B', 'G'))  # Side 0 to 2
        self.assertTrue(self.atm.is_valid_transition('C', 'J'))  # Side 0 to 3
        self.assertTrue(self.atm.is_valid_transition('E', 'H'))  # Side 1 to 2
        
        # Invalid transitions (same side)
        self.assertFalse(self.atm.is_valid_transition('A', 'B'))  # Both on side 0
        self.assertFalse(self.atm.is_valid_transition('D', 'E'))  # Both on side 1
        self.assertFalse(self.atm.is_valid_transition('G', 'I'))  # Both on side 2
        self.assertFalse(self.atm.is_valid_transition('J', 'L'))  # Both on side 3
    
    def test_case_insensitive_transitions(self):
        """Test that transitions work with different cases."""
        self.assertTrue(self.atm.is_valid_transition('a', 'd'))
        self.assertTrue(self.atm.is_valid_transition('A', 'd'))
        self.assertTrue(self.atm.is_valid_transition('a', 'D'))
        self.assertFalse(self.atm.is_valid_transition('a', 'b'))
    
    def test_invalid_letters(self):
        """Test transitions with invalid letters."""
        self.assertFalse(self.atm.is_valid_transition('A', 'Z'))  # Z not in puzzle
        self.assertFalse(self.atm.is_valid_transition('X', 'D'))  # X not in puzzle
        self.assertFalse(self.atm.is_valid_transition('', 'A'))   # Empty string
        self.assertFalse(self.atm.is_valid_transition('A', ''))   # Empty string
    
    def test_get_valid_next_letters(self):
        """Test getting valid next letters."""
        # From 'A' (side 0), can go to sides 1, 2, 3
        valid_next = self.atm.get_valid_next_letters('A')
        expected = {'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'}
        self.assertEqual(valid_next, expected)
        
        # From 'E' (side 1), can go to sides 0, 2, 3
        valid_next = self.atm.get_valid_next_letters('E')
        expected = {'A', 'B', 'C', 'G', 'H', 'I', 'J', 'K', 'L'}
        self.assertEqual(valid_next, expected)
        
        # Invalid letter
        valid_next = self.atm.get_valid_next_letters('Z')
        self.assertEqual(valid_next, set())
    
    def test_valid_word(self):
        """Test word validation."""
        # Valid words (alternating sides)
        self.assertTrue(self.atm.is_valid_word('AD'))    # Side 0 -> 1
        self.assertTrue(self.atm.is_valid_word('AGK'))   # Side 0 -> 2 -> 3
        self.assertTrue(self.atm.is_valid_word('ADGJ'))  # Side 0 -> 1 -> 2 -> 3
        
        # Invalid words (same side consecutive)
        self.assertFalse(self.atm.is_valid_word('AB'))   # Both side 0
        self.assertFalse(self.atm.is_valid_word('ADE'))  # A->D valid, D->E invalid (same side)
        
        # Single letters (should be valid if in puzzle)
        self.assertTrue(self.atm.is_valid_word('A'))
        self.assertFalse(self.atm.is_valid_word('Z'))
        
        # Empty word
        self.assertFalse(self.atm.is_valid_word(''))
    
    def test_get_unused_letters(self):
        """Test getting unused letters."""
        # No letters used
        unused = self.atm.get_unused_letters(set())
        self.assertEqual(unused, self.atm.all_letters)
        
        # Some letters used
        used = {'A', 'D', 'G'}
        unused = self.atm.get_unused_letters(used)
        expected = {'B', 'C', 'E', 'F', 'H', 'I', 'J', 'K', 'L'}
        self.assertEqual(unused, expected)
        
        # All letters used
        unused = self.atm.get_unused_letters(self.atm.all_letters)
        self.assertEqual(unused, set())
    
    def test_different_box_configuration(self):
        """Test with a different box configuration."""
        atm = LetterBoxATM(['XY', 'ZW', 'UV', 'ST'])
        
        # Test basic functionality
        self.assertEqual(atm.all_letters, {'X', 'Y', 'Z', 'W', 'U', 'V', 'S', 'T'})
        self.assertTrue(atm.is_valid_transition('X', 'Z'))   # Different sides
        self.assertFalse(atm.is_valid_transition('X', 'Y'))  # Same side
        
        # Test valid word
        self.assertTrue(atm.is_valid_word('XZ'))
        self.assertFalse(atm.is_valid_word('XY'))


if __name__ == '__main__':
    unittest.main()