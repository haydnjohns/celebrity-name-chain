

# Celebrity Name Chain

This project finds *celebrity name chains*—sequences of names where the **last name of one celebrity is the first name of the next**, forming either linear chains or loops. For example:
```

Michael Jordan → Jordan Peele → Peele Smith

````
---

### Quick Start

You **don’t need to run the scrapers** or fetch data yourself—it's already provided.

To jump straight to generating name chains or loops:

```bash
git clone https://github.com/your-username/celebrity-name-chain.git
cd celebrity-name-chain
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/create_chains.py <chain_type> <min_chain_length> <max_chain_length> <chain_outsputs_per_length>
````

Input arguments are:
```<chain_type> — either 'loop' or 'chain'
<min_length> — minimum chain/loop length (e.g. 3)
<max_length> — maximum chain/loop length (e.g. 7)
<max_per_length> — how many results to generate for each length (e.g. 5)
```

Example use:
```
python3 src/create_chains.py loop 3 5 2
```

Output:
```
=== Finding loops of length 3 ===
Found 2 loops
Loop 1: david lauren → lauren elizabeth → elizabeth david → david lauren
Loop 2: george will → will ryan → ryan george → george will

=== Finding loops of length 4 ===
Found 2 loops
Loop 1: paul rand → rand paul → paul taylor → taylor paul → paul rand
Loop 2: anderson cooper → cooper scott → scott cohen → cohen anderson → anderson cooper

=== Finding loops of length 5 ===
Found 2 loops
Loop 1: connor ryan → ryan george → george michael → michael jordan → jordan connor → connor ryan
Loop 2: george michael → michael morgan → morgan jean → jean paul → paul george → george michael
```

---

### How It Works (4 Steps)
  
The project has four main steps. **Only Step 4 is needed if you’re just using the project** — the other steps are included for transparency and customization.

|**Step**|**Description**|**File**|
|---|---|---|
|**1**|Count first-letter frequencies from U.S. baby names to bias name scraping|src/get_letter_counts.py|
|**2**|Scrape celebrity names from [thefamouspeople.com](https://www.thefamouspeople.com/) based on those frequencies|src/get_celebrity_names.py|
|**3**|Clean up names (e.g., remove initials, one-word names, names with more than 2 words)|src/clean_name_list.py|
|**4**|**Build chains and loops from the cleaned name list**|src/create_name_chains.py|

---

###  Project Structure

```
celebrity-name-chain
├── data                                 # Raw SSA baby name data (1880–2024)
│   ├── NationalReadMe.pdf
│   ├── yob1880.txt
│   ├── yob1881.txt
│   ├── yob1882.txt
│   ├── ...
│   ├── yob2022.txt
│   ├── yob2023.txt
│   └── yob2024.txt
├── outputs                            # Precomputed name lists and frequencies
│   ├── celebrity_list_all.json
│   ├── celebrity_list_cleaned.json
│   └── letter_counts.json
├── src                                # Core Python scripts
│   ├── clean_name_list.py
│   ├── config.py
│   ├── create_name_chains.py
│   ├── get_celebrity_names.py
│   ├── get_letter_counts.py
│   └── main.py              
├── .gitignore
├── requirements.txt
└── README.md
```

