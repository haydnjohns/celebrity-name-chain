import json
import os
from config import OUTPUT_DIR

"""
### STEP THREE ###

Cleans up the scraped list of celebrity names for processing.

STRICT MODE:
Keeps only names that are exactly "firstname lastname", excluding:
    - Single names (e.g., "Rihanna")
    - More than two names (e.g., "Paul Thomas Anderson")
    - Jr/Sr suffixes (e.g., "Robert Downey Jr.")
    - Names with initials (e.g., "H. P. Lovecraft")

NON-STRICT MODE:
Allows names with more than two parts (e.g., "Paul Thomas Anderson"),
but still excludes:
    - Names with initials
    - Names with Jr/Sr suffixes

All names are converted to lowercase.
"""

def clean_names(input_file, output_file, strict=False):
    # Load original names
    with open(input_file, "r", encoding="utf-8") as f:
        names = json.load(f)

    def is_valid_name(name):
        name_lower = name.lower()
        if "." in name or " jr" in name_lower or " sr" in name_lower:
            return False
        if strict:
            return name.count(" ") == 1  # Exactly two parts
        return True  # Allow more than two parts if not strict

    cleaned = []
    for name in names:
        if is_valid_name(name):
            parts = name.strip().split()
            cleaned_name = " ".join(part.lower() for part in parts)
            cleaned.append(cleaned_name)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save cleaned names
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Cleaned {len(cleaned)} names out of {len(names)}.")
    print(f"Saved cleaned names to '{output_file}'.")

if __name__ == "__main__":
    input_file = os.path.join(OUTPUT_DIR, "celebrity_list_all.json")
    output_file = os.path.join(OUTPUT_DIR, "celebrity_list_cleaned.json")
    clean_names(input_file, output_file, strict=False)  # Set to False for non-strict behavior