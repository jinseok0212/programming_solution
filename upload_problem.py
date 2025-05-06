import argparse
import datetime
import os
import subprocess

README_PATH = "README.md"

HEADER = "| No | Site | Title | Solution Link | Problem Link | Last Solve |"
SEPARATOR = "|----|------|-------|----------------|--------------|-------------|"

def load_readme():
    if not os.path.exists(README_PATH):
        with open(README_PATH, "w") as f:
            f.write(HEADER + "\n" + SEPARATOR + "\n")
    with open(README_PATH, "r") as f:
        return f.read().splitlines()

def save_readme(lines):
    with open(README_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")

def generate_row(no, site, title, filename, link):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    file_path = f"{site}/{filename}"
    solution_md = f"[{filename}]({file_path})"
    link_md = f"[문제 링크]({link})"
    return f"| {no} | {site} | {title} | {solution_md} | {link_md} | {now} |"

def git_commit_and_push(commit_message, filepath):
    try:
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "add", README_PATH], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("⚠️ Git command failed. Make sure you're in a Git repository and configured correctly.")

def is_valid_row(line):
    parts = line.split("|")
    try:
        int(parts[1].strip())  # No 필드가 숫자인지 검사
        return True
    except:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--link", required=True)

    args = parser.parse_args()

    number = os.path.splitext(args.filename)[0].split("_")[-1]  # e.g., boj_28278.c -> 28278
    readme_lines = load_readme()

    # Remove duplicates and keep only one header
    body = [line for line in readme_lines if HEADER not in line and SEPARATOR not in line]

    # Remove previous row with same number and site
    body = [line for line in body if not (line.startswith(f"| {number} ") and f"| {args.site} |" in line)]

    # Append new row
    row = generate_row(number, args.site, args.title, args.filename, args.link)
    body.append(row)

    # Sort by problem number descending
    rows = [line for line in body if is_valid_row(line)]
    others = [line for line in body if not is_valid_row(line)]
    sorted_rows = sorted(rows, key=lambda x: int(x.split("|")[1].strip()), reverse=True)

    final_lines = [HEADER, SEPARATOR] + sorted_rows
    save_readme(final_lines)
    print(f"✅ {args.filename} added to README.md")

    # Git commit & push
    file_path = f"{args.site}/{args.filename}"
    commit_msg = f"Add: {args.site.upper()} {args.title}"
    git_commit_and_push(commit_msg, file_path)

if __name__ == "__main__":
    main()
