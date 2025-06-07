import os
import argparse
from calculate_chains import create_name_chains

"""
designed for easy running from terminal but essentially does the same thing as create_chains_main/py
"""

def main():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_input_path = os.path.join(BASE_DIR, "outputs", "celebrity_list_cleaned.json")

    parser = argparse.ArgumentParser(
        description="Generate celebrity name chains or loops from a cleaned list."
    )
    parser.add_argument("chain_type", choices=["chain", "loop"], help="Type of sequence to generate.")
    parser.add_argument("min_length", type=int, help="Minimum chain/loop length.")
    parser.add_argument("max_length", type=int, help="Maximum chain/loop length.")
    parser.add_argument("max_per_length", type=int, help="Max chains/loops to generate per length.")

    args = parser.parse_args()

    create_name_chains(
        celebrity_list_path=default_input_path,
        chain_type=args.chain_type,
        min_length=args.min_length,
        max_length=args.max_length,
        max_chains_per_length=args.max_per_length
    )

if __name__ == "__main__":
    main()