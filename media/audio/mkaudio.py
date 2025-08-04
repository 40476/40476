#!/bin/python3
import os
import subprocess
import json
import random

# Settings
source_dir = os.getcwd()
config_path = "config.json"

# Load or initialize config
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
else:
    config = []

def generate_random_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def get_relative_path(filepath):
    parts = filepath.split(os.sep)
    return os.path.join(*parts[-3:]) if len(parts) >= 3 else filepath

def is_in_config_by_path(filepath):
    # Normalize path for consistent comparison
    rel_path = get_relative_path(filepath)
    return any(entry["location"] == rel_path for entry in config)

# Step 1: Process original files (skip "new-" and files that already have a converted version)
for filename in os.listdir(source_dir):
    if filename.startswith("new-") or not os.path.isfile(filename):
        continue

    new_filename = f"new-{filename}"
    new_path = os.path.join(source_dir, new_filename)

    if os.path.exists(new_path):
        print(f"removing '{filename}' — new version exists")
        os.remove(os.path.join(source_dir, filename))
        continue

    print(f"Processing '{filename}'...")
    try:
        subprocess.run(["ffmpeg", "-i", filename, "-af", "loudnorm", new_filename], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Failed to create '{new_filename}' — original retained")
        continue

    if os.path.exists(new_path):
        print(f"Removing original '{filename}'")
        os.remove(os.path.join(source_dir, filename))

# Step 2: Add unlisted "new-" files to config based on filepath
for filename in os.listdir(source_dir):
    if not filename.startswith("new-") or not os.path.isfile(filename):
        continue

    full_path = os.path.join(source_dir, filename)
    rel_path = get_relative_path(full_path)

    if is_in_config_by_path(full_path):
        continue

    entry = {
        "name": filename,
        "location": rel_path,
        "color": generate_random_hex()
    }
    config.append(entry)
    print(f"🆕 Added '{filename}' to config.")

# Step 3: Save updated config
with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print("✅ All done! Config updated.")
