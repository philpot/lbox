#!/usr/bin/env python3
"""
Trie (prefix tree) implementation for efficient word lookups.
Used to store and search the dictionary words for the Letter Boxed solver.
"""

class TrieNode:
    """A node in the Trie data structure."""
    
    def __init__(self):
        self.children = {}  # Dictionary mapping char -> TrieNode
        self.is_end_of_word = False


class Trie:
    """Trie (prefix tree) data structure for efficient word storage and lookup."""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert a word into the trie."""
        if not word:
            return
        
        word = word.lower()
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
    
    def search(self, word):
        """Check if a word exists in the trie."""
        if not word:
            return False
        
        word = word.lower()
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word in the trie starts with the given prefix."""
        if not prefix:
            return True
        
        prefix = prefix.lower()
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def get_node_for_prefix(self, prefix):
        """Get the TrieNode corresponding to a prefix, or None if not found."""
        if not prefix:
            return self.root
        
        prefix = prefix.lower()
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def load_from_file(self, filename):
        """Load words from a dictionary file into the trie."""
        count = 0
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    # Filter out words with non-alphabetic characters or too short
                    if word and word.isalpha() and len(word) >= 3:
                        self.insert(word)
                        count += 1
        except FileNotFoundError:
            print(f"Dictionary file {filename} not found")
            return 0
        
        return count