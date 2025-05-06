import argparse
import datetime
import os
import subprocess

README_PATH = "README.md"

HEADER = """| No | Site | Title | Solution Link | Problem Link | Last Solve |
|----|------|-------|----------------|--------------|-------------|"""

def load_readme():
    if not os.path.exists(README_PATH):
        with open(README_PATH, "w") as f:
            f.write(HEADER + "\n")
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

def git_commit_and_push(commit_message):
    try:
        subprocess.run(["git", "add", README_PATH], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("⚠️ Git command failed. Make sure you're in a Git repository and configured correctly.")

def is_valid_row(line):
    try:
        return line.startswith("| ") and int(line.split("|")[1].strip())
    except (IndexError, ValueError):
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

    # Remove any existing entry with the same number & site
    body = [line for line in readme_lines if not (line.startswith(f"| {number} ") and f"| {args.site} |" in line)]

    # Insert new row
    row = generate_row(number, args.site, args.title, args.filename, args.link)
    if HEADER not in body:
        body.insert(0, HEADER)
    body.append(row)

    # Sort only valid data rows (excluding header)
    header = [line for line in body if not is_valid_row(line)]
    rows = [line for line in body if is_valid_row(line)]
    body = header + sorted(rows, key=lambda x: datetime.datetime.strptime(x.split("|")[-2].strip(), "%Y-%m-%d %H:%M"), reverse=True)

    save_readme(body)
    print(f"✅ {args.filename} added to README.md")

    # Automatically commit and push changes
    commit_msg = f"Add: {args.site.upper()} {args.title}"
    git_commit_and_push(commit_msg)

if __name__ == "__main__":
    main()
