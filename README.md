# lbox
Solve NYT Letter Boxed puzzle using depth-first search through an ATM (Automaton)

## Overview

This project implements a solver for the New York Times Letter Boxed puzzle using:

- **Trie (Prefix Tree)**: Efficient storage and lookup of dictionary words
- **ATM (Automaton)**: Finite state machine governing valid letter transitions
- **Depth-First Search**: Explores possible word sequences to find complete solutions

## Letter Boxed Rules

The Letter Boxed puzzle consists of a square with letters arranged on each side. Players must:
1. Form words by connecting letters
2. Consecutive letters in a word cannot be from the same side of the box
3. Use all letters at least once to complete the puzzle
4. Each word must start with the last letter of the previous word (when chaining)

## Usage

### Command Line Interface

```bash
python main.py <side1> <side2> <side3> <side4> [options]
```

**Examples:**
```bash
# Basic usage with 4 sides
python main.py ABC DEF GHI JKL

# Limit to 3 words maximum, show only 5 solutions  
python main.py --max-words 3 --limit 5 ABC DEF GHI JKL

# Use custom dictionary
python main.py --dict /path/to/words.txt ABC DEF GHI JKL

# Set minimum word length to 4
python main.py --min-length 4 ABC DEF GHI JKL
```

**Options:**
- `--dict, --dictionary`: Dictionary file path (default: /usr/share/dict/american-english)
- `--max-words`: Maximum words in solution (default: 5)
- `--min-length`: Minimum word length (default: 3)
- `--limit`: Maximum solutions to display (default: 10)

### Python API

```python
from solver import LetterBoxSolver

# Create solver with box configuration
solver = LetterBoxSolver(['ABC', 'DEF', 'GHI', 'JKL'])

# Find solutions
solutions = solver.solve(max_words=4, min_word_length=3)

# Print results
solver.print_solutions(limit=10)
```

## Architecture

### Core Components

1. **Trie (`trie.py`)**: Prefix tree for efficient word storage and lookup
   - Insert words from dictionary
   - Check if word exists
   - Check if prefix has valid continuations

2. **LetterBoxATM (`letterbox_atm.py`)**: Automaton for transition rules
   - Validates letter-to-letter transitions
   - Ensures consecutive letters are on different sides
   - Tracks used/unused letters

3. **LetterBoxSolver (`solver.py`)**: Main solving logic
   - Loads dictionary into trie
   - Uses depth-first search to find word sequences
   - Validates solutions against puzzle constraints

### Algorithm

The solver uses depth-first search with the following strategy:

1. **Word Discovery**: For each starting letter, find all valid words using DFS through the trie while respecting ATM transition rules

2. **Solution Search**: Use DFS to build word sequences where:
   - Each word follows ATM transition rules
   - Next word starts with last letter of previous word
   - All puzzle letters are eventually used

3. **Pruning**: Early termination when:
   - No valid words can be formed with current prefix
   - Maximum word count reached without using all letters
   - Sufficient solutions found

## Installation

### Dictionary Setup

Install a word dictionary (Ubuntu/Debian):
```bash
sudo apt update && sudo apt install wamerican
```

This installs words to `/usr/share/dict/american-english`.

### Running the Solver

No additional dependencies required - uses only Python standard library:

```bash
cd lbox
python main.py ABC DEF GHI JKL
```

## Testing

Run the test suite:

```bash
# Test individual components
python test_trie.py
python test_letterbox_atm.py
python test_integration.py

# Or run all tests
python -m unittest discover
```

## Example Output

```
NYT Letter Boxed Solver
========================================
Loading dictionary from /usr/share/dict/american-english...
Loaded 74319 words into trie
Solving Letter Boxed puzzle with letters: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
Box configuration: ['AB', 'CD', 'EF', 'GH']

Found 100 solution(s):
1. achebe -> edged -> deaf (uses 8 letters)
   ✓ Complete solution!
2. beach -> hedged -> decaf (uses 8 letters)
   ✓ Complete solution!
3. beached -> deaf -> fag (uses 8 letters)
   ✓ Complete solution!
...
```

## License

Apache License 2.0 - see LICENSE file for details.