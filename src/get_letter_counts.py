import os
import json
from config import DATA_DIR, OUTPUT_DIR  # ✅ Proper import

"""
### STEP ONE ###

Creates normalized histogram of first letter of US baby names based on data from 1880 to 2024
found here: https://www.ssa.gov/oact/babynames/limits.html

Histogram is used to bias the list of celebrity names we scrape from online to ensure we are
getting popular celebrities that are well sampled, i.e., lots of celebrities with names starting with J
but not many with names starting with X.
"""

def count_name_starting_letters(source_data_folder_path, output_json_path):
    letter_counts = {}

    for filename in os.listdir(source_data_folder_path):
        if filename.endswith(".txt") and filename.startswith("yob"):
            file_path = os.path.join(source_data_folder_path, filename)
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) != 3:
                        continue  # Skip malformed lines
                    name, _, count = parts
                    first_letter = name[0].upper()
                    count = int(count)
                    letter_counts[first_letter] = letter_counts.get(first_letter, 0) + count

    # Sort and normalize
    sorted_counts = dict(sorted(letter_counts.items()))
    total = sum(sorted_counts.values())
    normalized_counts = {letter: count / total for letter, count in sorted_counts.items()}

    # Save normalized counts
    with open(output_json_path, "w") as json_file:
        json.dump(normalized_counts, json_file, indent=4)

    print(f"Normalized letter counts saved to '{output_json_path}'.")
    return sorted_counts  # Return absolute counts for histogram

def print_letter_histogram(letter_counts, max_bar_width=30):
    print("\nLETTER FREQUENCY HISTOGRAM:")
    max_count = max(letter_counts.values())

    for letter, count in letter_counts.items():
        bar_length = int((count / max_count) * max_bar_width)
        bar = "#" * bar_length
        print(f"{letter}: {bar}")

# Example usage
if __name__ == "__main__":
    frequency_output_path = os.path.join(OUTPUT_DIR, "letter_counts.json")
    letter_counts = count_name_starting_letters(DATA_DIR, frequency_output_path)
    print_letter_histogram(letter_counts)