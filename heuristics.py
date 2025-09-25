#!/usr/bin/env python3
"""
Heuristic-based state evaluation system for Letter Boxed solver.
"""

from abc import ABC, abstractmethod
from typing import List, Set, Dict, Optional
from collections import Counter


class SolverContext:
    """Context information available to heuristics for scoring."""
    
    def __init__(self, atm, all_letters: Set[str], valid_words_by_letter: Dict[str, List[str]]):
        self.atm = atm
        self.all_letters = all_letters
        self.valid_words_by_letter = valid_words_by_letter
        
        # Pre-compute letter frequencies in valid words for rarity scoring
        self.letter_frequencies = self._compute_letter_frequencies()
        
        # Pre-compute how many words start with each letter
        self.words_starting_with = {letter: len(words) 
                                  for letter, words in valid_words_by_letter.items()}
    
    def _compute_letter_frequencies(self) -> Counter:
        """Compute how often each letter appears in valid words."""
        frequencies = Counter()
        for words in self.valid_words_by_letter.values():
            for word in words:
                for letter in word.upper():
                    frequencies[letter] += 1
        return frequencies


class PartialSolution:
    """Represents a partial solution state in the search."""
    
    def __init__(self, words: List[str], used_letters: Set[str], current_ending: Optional[str] = None, target_letters: Optional[Set[str]] = None):
        self.words = words
        self.used_letters = used_letters
        self.current_ending = current_ending
        self.target_letters = target_letters or set()
        self._score: Optional[float] = None  # Cached score
    
    @property
    def is_complete(self) -> bool:
        """Check if this partial solution uses all required letters."""
        return len(self.used_letters) == len(self.target_letters) if hasattr(self, 'target_letters') else False
    
    @property
    def remaining_letters(self) -> Set[str]:
        """Get letters still needed to complete the solution."""
        if hasattr(self, 'target_letters'):
            return self.target_letters - self.used_letters
        return set()
    
    def add_word(self, word: str) -> 'PartialSolution':
        """Create new partial solution by adding a word."""
        word_upper = word.upper()
        new_used = self.used_letters | set(word_upper)
        new_words = self.words + [word]
        new_ending = word_upper[-1] if word_upper else None
        
        return PartialSolution(new_words, new_used, new_ending, self.target_letters)
    
    def __lt__(self, other):
        """For priority queue ordering - higher scores first."""
        return (self._score or 0) > (other._score or 0)
    
    def __repr__(self):
        return f"PartialSolution(words={self.words}, score={self._score})"


class WordHeuristic(ABC):
    """Abstract base class for word scoring heuristics."""
    
    @abstractmethod
    def score_word(self, word: str, context: SolverContext, partial: PartialSolution) -> float:
        """Score a word in the context of a partial solution."""
        pass


class StateHeuristic(ABC):
    """Abstract base class for partial solution state scoring."""
    
    @abstractmethod
    def score_state(self, partial: PartialSolution, context: SolverContext) -> float:
        """Score how promising a partial solution is for completion."""
        pass


class RareLetterHeuristic(WordHeuristic):
    """Prefer words that use rare/hard-to-manage letters from remaining set."""
    
    def score_word(self, word: str, context: SolverContext, partial: PartialSolution) -> float:
        word_upper = word.upper()
        remaining = partial.remaining_letters
        
        # Score based on rarity of letters used from remaining set
        score = 0.0
        for letter in word_upper:
            if letter in remaining:
                # Inverse frequency - rarer letters get higher scores
                freq = context.letter_frequencies[letter]
                score += 1.0 / (freq + 1)  # +1 to avoid division by zero
        
        return score


class LengthHeuristic(WordHeuristic):
    """Prefer longer words that cover more letters."""
    
    def score_word(self, word: str, context: SolverContext, partial: PartialSolution) -> float:
        word_upper = word.upper()
        remaining = partial.remaining_letters
        
        # Score based on how many remaining letters this word covers
        covered_remaining = len(set(word_upper) & remaining)
        return covered_remaining * len(word_upper)


class CommonEndingHeuristic(WordHeuristic):
    """Prefer words that end with letters having many continuation options."""
    
    def score_word(self, word: str, context: SolverContext, partial: PartialSolution) -> float:
        if not word:
            return 0.0
        
        ending_letter = word.upper()[-1]
        # Score based on how many words can continue from this ending
        return context.words_starting_with.get(ending_letter, 0)


class ProgressHeuristic(StateHeuristic):
    """Evaluate how efficiently a partial solution is progressing."""
    
    def score_state(self, partial: PartialSolution, context: SolverContext) -> float:
        if not partial.words:
            return 0.0
        
        # Efficiency: letters covered per word used
        letters_covered = len(partial.used_letters)
        words_used = len(partial.words)
        
        return letters_covered / words_used


class CompletionEstimateHeuristic(StateHeuristic):
    """Estimate how many additional words are needed to complete."""
    
    def score_state(self, partial: PartialSolution, context: SolverContext) -> float:
        remaining = partial.remaining_letters
        if not remaining:
            return float('inf')  # Complete solution gets highest score
        
        # Simple greedy estimate: find longest words that could cover remaining letters
        estimate = self._greedy_completion_estimate(remaining, context, partial.current_ending)
        
        # Return inverse of estimate (fewer words needed = higher score)
        return 1.0 / (estimate + 1)
    
    def _greedy_completion_estimate(self, remaining: Set[str], context: SolverContext, current_ending: Optional[str]) -> int:
        """Greedy estimate of minimum words needed to cover remaining letters."""
        if not remaining:
            return 0
        
        uncovered = remaining.copy()
        words_needed = 0
        current_letter = current_ending
        
        while uncovered and words_needed < 10:  # Avoid infinite loops
            best_word = None
            best_coverage = 0
            
            # Find word starting with current_letter that covers most uncovered letters
            candidates = context.valid_words_by_letter.get(current_letter, []) if current_letter else []
            if not candidates:
                # If no continuation, try any remaining letter
                for letter in uncovered:
                    candidates.extend(context.valid_words_by_letter.get(letter, []))
            
            for word in candidates[:20]:  # Limit search for performance
                word_upper = word.upper()
                coverage = len(set(word_upper) & uncovered)
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_word = word
            
            if not best_word:
                return 10  # Pessimistic estimate if no valid continuation
            
            # Use best word
            word_upper = best_word.upper()
            uncovered -= set(word_upper)
            current_letter = word_upper[-1]
            words_needed += 1
        
        return words_needed


class CompositeHeuristic:
    """Combines multiple heuristics with weights."""
    
    def __init__(self, word_heuristics: List[tuple], state_heuristics: List[tuple]):
        """
        Args:
            word_heuristics: List of (heuristic, weight) tuples for word scoring
            state_heuristics: List of (heuristic, weight) tuples for state scoring
        """
        self.word_heuristics = word_heuristics
        self.state_heuristics = state_heuristics
    
    def score_word(self, word: str, context: SolverContext, partial: PartialSolution) -> float:
        """Combined score for a word."""
        total = 0.0
        for heuristic, weight in self.word_heuristics:
            total += weight * heuristic.score_word(word, context, partial)
        return total
    
    def score_state(self, partial: PartialSolution, context: SolverContext) -> float:
        """Combined score for a partial solution state."""
        total = 0.0
        for heuristic, weight in self.state_heuristics:
            total += weight * heuristic.score_state(partial, context)
        return total
    
    def score_partial_solution(self, partial: PartialSolution, context: SolverContext) -> float:
        """Overall score combining state evaluation."""
        return self.score_state(partial, context)