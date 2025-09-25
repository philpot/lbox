#!/usr/bin/env python3
"""
Letter Boxed puzzle solver CLI.
"""

import sys
import argparse
from solver import LetterBoxSolver


def main():
    """Main CLI interface for the Letter Boxed solver."""
    parser = argparse.ArgumentParser(
        description="Solve NYT Letter Boxed puzzle using depth-first search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ABC DEF GHI JKL
  python main.py --dict /usr/share/dict/words --max-words 3 ABC DEF GHI JKL
  
The puzzle consists of a square box with letters on each side.
You must form words by connecting letters, but consecutive letters
cannot be from the same side of the box.
"""
    )
    
    parser.add_argument(
        'sides',
        nargs=4,
        help='Four sides of the letter box (e.g., ABC DEF GHI JKL)'
    )
    
    parser.add_argument(
        '--dict', '--dictionary',
        default='/usr/share/dict/american-english',
        help='Dictionary file to use (default: /usr/share/dict/american-english)'
    )
    
    parser.add_argument(
        '--max-words',
        type=int,
        default=5,
        help='Maximum number of words in solution (default: 5)'
    )
    
    parser.add_argument(
        '--min-length',
        type=int,
        default=3,
        help='Minimum word length (default: 3)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of solutions to display (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Validate sides
    for i, side in enumerate(args.sides):
        if not side.isalpha():
            print(f"Error: Side {i+1} '{side}' contains non-alphabetic characters")
            sys.exit(1)
        if len(side) < 1:
            print(f"Error: Side {i+1} is empty")
            sys.exit(1)
    
    print("NYT Letter Boxed Solver")
    print("=" * 40)
    
    try:
        # Create and run solver
        solver = LetterBoxSolver(args.sides, args.dict)
        solutions = solver.solve(args.max_words, args.min_length)
        solver.print_solutions(args.limit)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Try installing a word dictionary with: sudo apt install wamerican")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nSearch interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()