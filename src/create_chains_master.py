from colorama import init, Fore
from get_celebrity_names import get_celebrity_names
from get_letter_counts import count_name_starting_letters, print_letter_histogram
from clean_name_list import clean_names
import calculate_chains as chain
import os
from config import DATA_DIR, OUTPUT_DIR

# === CONFIGURATION === #
RUN_STEP_1 = False   # Count letter frequencies from real name dataset
RUN_STEP_2 = False  # Scrape celebrity names
RUN_STEP_3 = False   # Clean the scraped names
RUN_STEP_4 = True   # Generate name chains or loops

# === INPUTS === #
name_frequency_folder_path = DATA_DIR
frequency_output_json = os.path.join(OUTPUT_DIR, "letter_counts.json")

total_celebrities = 25000  # Can go up to ~25,000 (the size of the database)
celebrity_list_output_json = os.path.join(OUTPUT_DIR, "celebrity_list_all.json")
cleaned_celebrity_output = os.path.join(OUTPUT_DIR, "celebrity_list_cleaned.json")
raw_celebrity_list_input = celebrity_list_output_json  # reusing scraped output

celebrity_list_path = cleaned_celebrity_output  # for chaining
chain_type = "loop"  # "chain" or "loop"
min_length = 3
max_length = 5
max_chains_per_length = 2

# === STEP FUNCTIONS === #

# Initialize colorama
init(autoreset=True)

def step_1_count_letter_frequencies():
    print(Fore.BLUE + "\nSTEP 1: COUNTING NAME-STARTING LETTERS...\n")
    letter_counts = count_name_starting_letters(name_frequency_folder_path, frequency_output_json)
    print_letter_histogram(letter_counts)

def step_2_scrape_celebrities():
    print(Fore.BLUE + "\nSTEP 2: SCRAPING CELEBRITY NAMES...\n")
    get_celebrity_names(total_celebrities, celebrity_list_output_json, frequency_output_json)

def step_3_clean_names():
    print(Fore.BLUE + "\nSTEP 3: CLEANING NAME LIST...\n")
    clean_names(raw_celebrity_list_input, cleaned_celebrity_output)

def step_4_create_chains():
    print(Fore.BLUE + "\nSTEP 4: CREATING NAME CHAINS...\n")
    chain.create_name_chains(
        celebrity_list_path,
        chain_type,
        min_length,
        max_length,
        max_chains_per_length
    )

# === MAIN RUNNER === #

if __name__ == "__main__":
    if RUN_STEP_1:
        step_1_count_letter_frequencies()

    if RUN_STEP_2:
        step_2_scrape_celebrities()

    if RUN_STEP_3:
        step_3_clean_names()

    if RUN_STEP_4:
        step_4_create_chains()