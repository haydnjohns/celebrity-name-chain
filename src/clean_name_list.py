import json
import os
from config import OUTPUT_DIR

"""
### STEP THREE ###

Cleans up the scraped list of celebrity names for processing.
Keeps only names that are exactly "firstname lastname", excluding:
    - Single names (e.g., "Rihanna")
    - More than two names (e.g., "Paul Thomas Anderson")
    - Jr/Sr suffixes (e.g., "Robert Downey Jr.")
    - Names with initials (e.g., "H. P. Lovecraft")
Converts all names to lowercase.
"""

def clean_names(input_file, output_file):
    # Load original names
    with open(input_file, "r", encoding="utf-8") as f:
        names = json.load(f)

    def is_valid_name(name):
        return (
            name.count(" ") == 1 and  # exactly two words
            "." not in name and       # no initials
            not any(suffix in name.lower() for suffix in [" jr", " sr"])  # exclude Jr/Sr
        )

    cleaned = []
    for name in names:
        if is_valid_name(name):
            first, last = name.split()
            cleaned_name = f"{first.lower()} {last.lower()}"
            cleaned.append(cleaned_name)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save cleaned names
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Cleaned {len(cleaned)} names out of {len(names)}.")
    print(f"Saved cleaned names to '{output_file}'.")

if __name__ == "__main__":
    input_file = os.path.join(OUTPUT_DIR, "celebrity_list_long_all.json")
    output_file = os.path.join(OUTPUT_DIR, "celebrity_list_long_cleaned.json")
    clean_names(input_file, output_file)