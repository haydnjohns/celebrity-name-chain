import os

# This gives you the root of the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# print(f"DATA_DIR: {DATA_DIR}")
# print(f"OUTPUT_DIR: {OUTPUT_DIR}")
# print(f"BASE_DIR: {BASE_DIR}")