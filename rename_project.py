"""
Script to replace 'TQM Pharm Enterprise' with 'TQM Pharm Enterprise' everywhere across the repository.
"""

import os
import glob
import shutil

REPLACEMENTS = [
    ("TQM PHARM ENTERPRISE", "TQM PHARM ENTERPRISE"),
    ("TQM Pharm Enterprise", "TQM Pharm Enterprise"),
    ("TQM PHARM", "TQM PHARM"),
    ("TQM Pharm", "TQM Pharm"),
    ("tqmpharm", "tqmpharm"),
    ("SRS_TQM Pharm_Enterprise", "SRS_TQM_Pharm_Enterprise"),
    ("TQM Pharm_TQM_Presentation_Piyush_Bhatt", "TQM_Pharm_Presentation_Piyush_Bhatt"),
]

EXTENSIONS = [".py", ".html", ".json", ".md", ".txt", ".csv"]

def should_process(file_path):
    if any(p in file_path for p in [".git", "__pycache__", ".pytest_cache", ".idea", "backups", "pharmacy.db"]):
        return False
    _, ext = os.path.splitext(file_path)
    return ext in EXTENSIONS

def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        except Exception as e:
            print(f"Skipping {file_path}: {e}")
            return False

    orig_content = content
    for old_str, new_str in REPLACEMENTS:
        content = content.replace(old_str, new_str)

    if content != orig_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {file_path}")
        return True
    return False

def main():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    updated_count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip blacklisted directories
        if any(b in dirpath for b in [".git", "__pycache__", ".pytest_cache", ".idea", "backups"]):
            continue
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            if should_process(fpath):
                if process_file(fpath):
                    updated_count += 1
    print(f"\nTotal text files updated: {updated_count}")

    # Rename SRS markdown file if it exists
    old_srs_md = os.path.join(root_dir, "SRS_TQM Pharm_Enterprise.md")
    new_srs_md = os.path.join(root_dir, "SRS_TQM_Pharm_Enterprise.md")
    if os.path.exists(old_srs_md):
        shutil.copy2(old_srs_md, new_srs_md)
        print(f"Created {new_srs_md}")

if __name__ == "__main__":
    main()
