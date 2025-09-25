#!/usr/bin/env python3
"""
Improved Letter Boxed solver using best-first search with heuristic evaluation.
"""

import heapq
import time
from typing import List, Set, Dict, Optional
from collections import defaultdict

from trie import Trie
from letterbox_atm import LetterBoxATM
from heuristics import (
    SolverContext, PartialSolution, CompositeHeuristic,
    RareLetterHeuristic, LengthHeuristic, CommonEndingHeuristic,
    ProgressHeuristic, CompletionEstimateHeuristic
)


class BestFirstLetterBoxSolver:
    """
    Advanced Letter Boxed solver using best-first search with intelligent heuristics.
    """
    
    def __init__(self, sides, dictionary_file="/usr/share/dict/american-english"):
        """Initialize the solver with heuristic-based search."""
        self.atm = LetterBoxATM(sides)
        self.trie = Trie()
        self.dictionary_file = dictionary_file
        self.solutions = []
        
        print(f"Loading dictionary from {dictionary_file}...")
        word_count = self.trie.load_from_file(dictionary_file)
        print(f"Loaded {word_count} words into trie")
        
        # Pre-compute valid words for each starting letter
        print("Pre-computing valid words by starting letter...")
        self.valid_words_by_letter = self._precompute_valid_words()
        
        # Initialize solver context for heuristics
        self.context = SolverContext(self.atm, self.atm.all_letters, self.valid_words_by_letter)
        
        # Set up default heuristic combination
        self.heuristic = self._create_default_heuristic()
        
        print("Solver initialization complete.")
    
    def _precompute_valid_words(self, min_length=3, max_length=15) -> Dict[str, List[str]]:
        """Pre-compute all valid words grouped by starting letter."""
        valid_words = defaultdict(list)
        
        # Get all words from trie and filter by ATM validity
        total_words = 0
        valid_count = 0
        
        # Read dictionary file directly to get all words
        try:
            with open(self.dictionary_file, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    total_words += 1
                    
                    if min_length <= len(word) <= max_length and word.isalpha():
                        # Check if word uses only puzzle letters and follows ATM rules
                        if self._is_valid_puzzle_word(word):
                            start_letter = word[0].upper()
                            valid_words[start_letter].append(word)
                            valid_count += 1
        except FileNotFoundError:
            print(f"Error: Dictionary file {self.dictionary_file} not found")
            
        print(f"Pre-computed {valid_count} valid words from {total_words} total words")
        
        # Sort words by length (descending) to prioritize longer words
        for letter in valid_words:
            valid_words[letter].sort(key=len, reverse=True)
        
        return dict(valid_words)
    
    def _is_valid_puzzle_word(self, word: str) -> bool:
        """Check if a word can be formed according to puzzle rules."""
        return self.atm.is_valid_word(word)
    
    def _create_default_heuristic(self) -> CompositeHeuristic:
        """Create a balanced default heuristic combination."""
        word_heuristics = [
            (RareLetterHeuristic(), 1.0),
            (LengthHeuristic(), 2.0),
            (CommonEndingHeuristic(), 0.5)
        ]
        
        state_heuristics = [
            (ProgressHeuristic(), 3.0),
            (CompletionEstimateHeuristic(), 5.0)
        ]
        
        return CompositeHeuristic(word_heuristics, state_heuristics)
    
    def solve(self, max_words=5, time_limit=30.0) -> List[List[str]]:
        """
        Solve using best-first search with heuristic evaluation.
        
        Args:
            max_words: Maximum words in solution (for pruning)
            time_limit: Maximum time to spend searching (seconds)
        
        Returns:
            List of solution word sequences, sorted by quality
        """
        self.solutions = []
        start_time = time.time()
        
        print(f"Starting best-first search (max_words={max_words}, time_limit={time_limit}s)")
        print(f"Puzzle letters: {sorted(self.atm.all_letters)}")
        print(f"Box configuration: {self.atm.sides}")
        
        # Priority queue of partial solutions to explore
        # Use negative score for min-heap (want highest scores first)
        search_queue = []
        
        # Initialize with empty solution
        initial_state = PartialSolution([], set(), None, self.atm.all_letters)
        initial_score = self.heuristic.score_partial_solution(initial_state, self.context)
        initial_state._score = initial_score
        
        heapq.heappush(search_queue, initial_state)
        
        best_solution_length = float('inf')
        states_explored = 0
        
        while search_queue and time.time() - start_time < time_limit:
            current_state = heapq.heappop(search_queue)
            states_explored += 1
            
            # Check if this is a complete solution
            if current_state.is_complete:
                self.solutions.append(current_state.words[:])
                solution_length = len(current_state.words)
                
                if solution_length < best_solution_length:
                    best_solution_length = solution_length
                    print(f"Found solution with {solution_length} words: {current_state.words}")
                
                # Continue searching for better solutions
                continue
            
            # Prune if this branch cannot improve on best solution
            if len(current_state.words) >= min(max_words, best_solution_length):
                continue
            
            # Generate next possible states
            self._expand_state(current_state, search_queue, best_solution_length)
            
            # Progress reporting
            if states_explored % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"Explored {states_explored} states in {elapsed:.1f}s, queue size: {len(search_queue)}")
        
        elapsed = time.time() - start_time
        print(f"Search completed: {states_explored} states explored in {elapsed:.2f}s")
        
        # Sort solutions by length (fewer words better)
        self.solutions.sort(key=len)
        return self.solutions
    
    def _expand_state(self, state: PartialSolution, search_queue: list, best_length: int):
        """Generate and queue next possible states from current state."""
        # Determine valid starting letters for next word
        if state.current_ending:
            # Must start with last letter of previous word
            possible_starts = [state.current_ending]
        else:
            # First word can start with any letter
            possible_starts = list(self.atm.all_letters)
        
        for start_letter in possible_starts:
            candidate_words = self.valid_words_by_letter.get(start_letter, [])
            
            # Score ALL candidate words - let BFS priority queue handle selection
            scored_words = []
            for word in candidate_words:  # No arbitrary limit - score them all
                word_score = self.heuristic.score_word(word, self.context, state)
                scored_words.append((word_score, word))
            
            # Sort by score (descending) and add ALL to queue - let priority queue decide
            scored_words.sort(reverse=True)
            
            for word_score, word in scored_words:  # No arbitrary cutoff - add all viable words
                new_state = state.add_word(word)
                
                # Skip if no progress (word doesn't add new letters)
                if len(new_state.used_letters) <= len(state.used_letters):
                    continue
                
                # Skip if this branch can't beat best solution
                if len(new_state.words) >= best_length:
                    continue
                
                # Score the new state
                state_score = self.heuristic.score_partial_solution(new_state, self.context)
                new_state._score = state_score
                
                heapq.heappush(search_queue, new_state)
    
    def print_solutions(self, limit=10):
        """Print found solutions with analysis."""
        if not self.solutions:
            print("No solutions found.")
            return
        
        print(f"\nFound {len(self.solutions)} solution(s):")
        for i, solution in enumerate(self.solutions[:limit]):
            used_letters = set()
            for word in solution:
                used_letters.update(word.upper())
            
            print(f"{i+1}. {' -> '.join(solution)} ({len(solution)} words, {len(used_letters)} letters)")
            
            if len(used_letters) == len(self.atm.all_letters):
                print("   ✓ Complete solution!")
            else:
                missing = self.atm.all_letters - used_letters
                print(f"   Missing letters: {sorted(missing)}")
        
        if len(self.solutions) > limit:
            print(f"... and {len(self.solutions) - limit} more solutions")
    
    def set_heuristic_weights(self, rare_letter_weight=1.0, length_weight=2.0, 
                            common_ending_weight=0.5, progress_weight=3.0, 
                            completion_weight=5.0):
        """Allow customization of heuristic weights."""
        word_heuristics = [
            (RareLetterHeuristic(), rare_letter_weight),
            (LengthHeuristic(), length_weight),
            (CommonEndingHeuristic(), common_ending_weight)
        ]
        
        state_heuristics = [
            (ProgressHeuristic(), progress_weight),
            (CompletionEstimateHeuristic(), completion_weight)
        ]
        
        self.heuristic = CompositeHeuristic(word_heuristics, state_heuristics)
        print("Updated heuristic weights")