#!/usr/bin/env python3
"""
Depth-first search solver for Letter Boxed puzzle.
"""

from trie import Trie
from letterbox_atm import LetterBoxATM


class LetterBoxSolver:
    """
    Solver for Letter Boxed puzzle using depth-first search through an ATM.
    """
    
    def __init__(self, sides, dictionary_file="/usr/share/dict/american-english"):
        """
        Initialize the solver.
        
        Args:
            sides: List of 4 strings representing the box sides
            dictionary_file: Path to dictionary file
        """
        self.atm = LetterBoxATM(sides)
        self.trie = Trie()
        self.dictionary_file = dictionary_file
        self.solutions = []
        
        print(f"Loading dictionary from {dictionary_file}...")
        word_count = self.trie.load_from_file(dictionary_file)
        print(f"Loaded {word_count} words into trie")
    
    def find_words_starting_with(self, letter, min_length=3, max_length=15):
        """
        Find all valid words that start with the given letter.
        
        Args:
            letter: Starting letter
            min_length: Minimum word length
            max_length: Maximum word length to search
            
        Returns:
            list: List of valid words starting with letter
        """
        words = []
        self._dfs_words(letter.upper(), letter.upper(), words, min_length, max_length)
        return words[:50]  # Limit to first 50 words to avoid excessive computation
    
    def _dfs_words(self, current_path, current_letter, words, min_length, max_length=15):
        """
        Depth-first search to find words starting from current state.
        """
        # Limit word length to avoid infinite recursion
        if len(current_path) > max_length:
            return
            
        # Check if current path is a valid word
        if len(current_path) >= min_length and self.trie.search(current_path.lower()):
            words.append(current_path.lower())
        
        # If no words can start with this prefix, prune
        if not self.trie.starts_with(current_path.lower()):
            return
        
        # Try extending with valid next letters
        valid_next = self.atm.get_valid_next_letters(current_letter)
        for next_letter in sorted(valid_next):  # Sort for consistent ordering
            self._dfs_words(current_path + next_letter, next_letter, words, min_length, max_length)
    
    def solve(self, max_words=5, min_word_length=3):
        """
        Solve the Letter Boxed puzzle using depth-first search.
        
        Args:
            max_words: Maximum number of words in solution
            min_word_length: Minimum length for each word
            
        Returns:
            list: List of solution word sequences
        """
        self.solutions = []
        all_letters = self.atm.all_letters
        
        print(f"Solving Letter Boxed puzzle with letters: {sorted(all_letters)}")
        print(f"Box configuration: {self.atm.sides}")
        
        # Start DFS from each possible starting letter
        for start_letter in sorted(all_letters):
            self._dfs_solve([], set(), start_letter, max_words, min_word_length, all_letters)
        
        # Sort solutions by number of words (fewer is better)
        self.solutions.sort(key=len)
        return self.solutions
    
    def _dfs_solve(self, word_sequence, used_letters, current_letter, max_words, min_word_length, target_letters, depth=0):
        """
        Recursive depth-first search for complete solutions.
        """
        # Limit recursion depth to avoid infinite loops
        if depth > 20:
            return
            
        # If we've used all letters, we found a solution
        if used_letters == target_letters:
            self.solutions.append(word_sequence[:])
            return
        
        # If we've reached max words, stop
        if len(word_sequence) >= max_words:
            return
        
        # Early termination if we have enough solutions
        if len(self.solutions) >= 100:
            return

        # Find words starting with current_letter (or any letter if starting)
        if not word_sequence:  # Starting state
            start_letters = sorted(target_letters)[:6]  # Limit starting letters for performance
        else:
            # Must start with last letter of previous word
            start_letters = [current_letter]
        
        for start_letter in start_letters:
            words = self.find_words_starting_with(start_letter, min_word_length)
            
            for word in words[:20]:  # Limit words tried per starting letter
                word_upper = word.upper()
                
                # Check if word uses only puzzle letters and follows ATM rules
                if not self.atm.is_valid_word(word):
                    continue
                
                # Calculate new used letters
                word_letters = set(word_upper)
                new_used = used_letters | word_letters
                
                # Only proceed if we're making progress (using new letters)
                if len(new_used) <= len(used_letters):
                    continue
                
                # Add word to sequence and continue search
                word_sequence.append(word)
                last_letter = word_upper[-1]
                self._dfs_solve(word_sequence, new_used, last_letter, max_words, min_word_length, target_letters, depth + 1)
                word_sequence.pop()
                
                # Early termination if we have enough solutions
                if len(self.solutions) >= 100:
                    return
    
    def print_solutions(self, limit=10):
        """Print found solutions."""
        if not self.solutions:
            print("No solutions found.")
            return
        
        print(f"\nFound {len(self.solutions)} solution(s):")
        for i, solution in enumerate(self.solutions[:limit]):
            used_letters = set()
            for word in solution:
                used_letters.update(word.upper())
            
            print(f"{i+1}. {' -> '.join(solution)} (uses {len(used_letters)} letters)")
            
            if len(used_letters) == len(self.atm.all_letters):
                print("   ✓ Complete solution!")
            else:
                missing = self.atm.all_letters - used_letters
                print(f"   Missing letters: {sorted(missing)}")
        
        if len(self.solutions) > limit:
            print(f"... and {len(self.solutions) - limit} more solutions")