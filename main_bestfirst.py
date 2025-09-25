#!/usr/bin/env python3
"""
Letter Boxed puzzle solver CLI using the new best-first search algorithm.
"""

import sys
import argparse
from best_first_solver import BestFirstLetterBoxSolver


def main():
    """Main CLI interface for the improved Letter Boxed solver."""
    parser = argparse.ArgumentParser(
        description="Solve NYT Letter Boxed puzzle using best-first search with heuristics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_bestfirst.py ILA OCG FDR NTP
  python main_bestfirst.py --dict /usr/share/dict/words --max-words 2 ILA OCG FDR NTP
  python main_bestfirst.py --time-limit 30 --rare-weight 2.0 ILA OCG FDR NTP
  
The puzzle consists of a square box with letters on each side.
You must form words by connecting letters, but consecutive letters
cannot be from the same side of the box.
"""
    )
    
    parser.add_argument(
        'sides',
        nargs=4,
        help='Four sides of the letter box (e.g., ILA OCG FDR NTP)'
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
        '--time-limit',
        type=float,
        default=30.0,
        help='Maximum search time in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of solutions to display (default: 10)'
    )
    
    # Heuristic weight arguments
    parser.add_argument(
        '--rare-weight',
        type=float,
        default=1.0,
        help='Weight for rare letter heuristic (default: 1.0)'
    )
    
    parser.add_argument(
        '--length-weight',
        type=float,
        default=2.0,
        help='Weight for word length heuristic (default: 2.0)'
    )
    
    parser.add_argument(
        '--ending-weight',
        type=float,
        default=0.5,
        help='Weight for common ending heuristic (default: 0.5)'
    )
    
    parser.add_argument(
        '--progress-weight',
        type=float,
        default=3.0,
        help='Weight for progress heuristic (default: 3.0)'
    )
    
    parser.add_argument(
        '--completion-weight',
        type=float,
        default=5.0,
        help='Weight for completion estimate heuristic (default: 5.0)'
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
    
    print("NYT Letter Boxed Solver (Best-First Search)")
    print("=" * 50)
    
    try:
        # Create and configure solver
        solver = BestFirstLetterBoxSolver(args.sides, args.dict)
        
        # Set custom heuristic weights if provided
        solver.set_heuristic_weights(
            rare_letter_weight=args.rare_weight,
            length_weight=args.length_weight,
            common_ending_weight=args.ending_weight,
            progress_weight=args.progress_weight,
            completion_weight=args.completion_weight
        )
        
        # Solve the puzzle
        solutions = solver.solve(args.max_words, args.time_limit)
        solver.print_solutions(args.limit)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Try installing a word dictionary or check the dictionary path")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nSearch interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()