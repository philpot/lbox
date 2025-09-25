#!/usr/bin/env python3
"""
Letter Boxed puzzle ATM (Automaton) implementation.
Defines the state machine for valid letter transitions in the puzzle.
"""

class LetterBoxATM:
    """
    Automaton for Letter Boxed puzzle transitions.
    
    The puzzle consists of a square box with letters on each side.
    Valid transitions are from any letter to any letter NOT on the same side.
    """
    
    def __init__(self, sides):
        """
        Initialize the ATM with the box configuration.
        
        Args:
            sides: List of 4 strings, each representing letters on one side of the box.
                  E.g., ['ABC', 'DEF', 'GHI', 'JKL']
        """
        self.sides = [side.upper() for side in sides]
        self.letter_to_side = {}
        self.all_letters = set()
        
        # Build mapping from letter to side index
        for side_idx, side in enumerate(self.sides):
            for letter in side:
                self.letter_to_side[letter] = side_idx
                self.all_letters.add(letter)
    
    def is_valid_transition(self, from_letter, to_letter):
        """
        Check if a transition from one letter to another is valid.
        
        Args:
            from_letter: Starting letter
            to_letter: Target letter
            
        Returns:
            bool: True if transition is valid (letters on different sides)
        """
        if not from_letter or not to_letter:
            return False
        
        from_letter = from_letter.upper()
        to_letter = to_letter.upper()
        
        # Both letters must exist in the puzzle
        if from_letter not in self.letter_to_side or to_letter not in self.letter_to_side:
            return False
        
        # Letters must be on different sides
        return self.letter_to_side[from_letter] != self.letter_to_side[to_letter]
    
    def get_valid_next_letters(self, current_letter):
        """
        Get all letters that can follow the current letter.
        
        Args:
            current_letter: The current letter
            
        Returns:
            set: Set of letters that can follow current_letter
        """
        if not current_letter or current_letter.upper() not in self.letter_to_side:
            return set()
        
        current_letter = current_letter.upper()
        current_side = self.letter_to_side[current_letter]
        
        # Return all letters NOT on the current side
        valid_letters = set()
        for letter, side in self.letter_to_side.items():
            if side != current_side:
                valid_letters.add(letter)
        
        return valid_letters
    
    def is_valid_word(self, word):
        """
        Check if a word follows valid transition rules.
        
        Args:
            word: String to validate
            
        Returns:
            bool: True if all transitions in the word are valid
        """
        if not word or len(word) < 2:
            return len(word) == 1 and word.upper() in self.all_letters
        
        word = word.upper()
        
        # Check if all letters exist in puzzle
        for letter in word:
            if letter not in self.all_letters:
                return False
        
        # Check transitions
        for i in range(len(word) - 1):
            if not self.is_valid_transition(word[i], word[i + 1]):
                return False
        
        return True
    
    def get_unused_letters(self, used_letters):
        """
        Get letters that haven't been used yet.
        
        Args:
            used_letters: Set of letters that have been used
            
        Returns:
            set: Set of unused letters
        """
        used_upper = {letter.upper() for letter in used_letters}
        return self.all_letters - used_upper
    
    def __repr__(self):
        """String representation of the ATM."""
        return f"LetterBoxATM(sides={self.sides})"