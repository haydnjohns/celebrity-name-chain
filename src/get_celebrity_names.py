import requests
from bs4 import BeautifulSoup
import time
import string
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os
from config import OUTPUT_DIR
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

"""
STEP TWO
Scrapes celebrity names from this online database:
https://www.thefamouspeople.com/starting-x.php

Takes total number of celebrity names as an argument and distributes according to 
the first letter frequency json file (precomputed).
"""

def get_celebrities_by_letter(letter, limit):
    url = "https://www.thefamouspeople.com/ajax/page_loader.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": f"https://www.thefamouspeople.com/starting-{letter}.php",
    }

    names = []
    offset = 0
    seen = set()
    page_size = 100

    while len(names) < limit:
        payload = (
            f"action=scrollpagination"
            f"&number={page_size}"
            f"&offset={offset}"
            f"&sqlc=%5B%22a.name+LIKE+{letter}%25%22%5D"
            f"&c1=ALPHA&c2=&c3=&c4=____1"
        )

        response = requests.post(url, data=payload, headers=headers)
        if not response.ok or not response.text.strip():
            break

        soup = BeautifulSoup(response.text, "html.parser")
        anchors = soup.select("a.tileLink")

        if not anchors:
            break

        for a in anchors:
            name = a.get_text(strip=True)
            if name and name not in seen:
                names.append(name)
                seen.add(name)
            if len(names) >= limit:
                break

        offset += page_size
        time.sleep(0.5)  # Be polite to the server

    return letter, names

def get_celebrity_names(total_celebrities, output_path, letter_counts_path):
    with open(letter_counts_path, "r") as f:
        popularity = json.load(f)

    counts_per_letter = {
        letter.lower(): max(1, int(total_celebrities * popularity.get(letter.upper(), 0)))
        for letter in string.ascii_lowercase
    }

    all_results = {}
    start_all = time.time()

    with ThreadPoolExecutor(max_workers=13) as executor:
        futures = {
            executor.submit(get_celebrities_by_letter, letter, limit): letter
            for letter, limit in counts_per_letter.items()
        }



        for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=Fore.WHITE + "Scraping letters",
        ):
            letter, names = future.result()
            all_results[letter] = names

    elapsed_all = time.time() - start_all
    print(f"\nFinished scraping {total_celebrities} celebrities in {elapsed_all:.2f} seconds.")

    combined_names = []
    for letter in string.ascii_lowercase:
        combined_names.extend(all_results.get(letter, []))
    combined_names = sorted(set(combined_names))  # Remove duplicates

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_names, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(combined_names)} celebrity names to {output_path}")
    return all_results

# === Manual test run === #
if __name__ == "__main__":
    total_celebrities = 1000
    celebrity_list_output_json = os.path.join(OUTPUT_DIR, "celebrity_list_short_all.json")
    frequency_input_json = os.path.join(OUTPUT_DIR, "letter_counts.json")
    get_celebrity_names(total_celebrities, celebrity_list_output_json, frequency_input_json)