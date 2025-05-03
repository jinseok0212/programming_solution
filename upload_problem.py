import argparse
import datetime
import os
import subprocess

README_FILE = "README.md"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Upload solved problem to GitHub with README update.")
    parser.add_argument("--site", required=True, choices=["boj", "programmers"], help="boj or programmers")
    parser.add_argument("--title", required=True, help="Problem title")
    parser.add_argument("--filename", required=True, help="Source code filename (e.g., sol_001.c)")
    parser.add_argument("--link", required=True, help="Problem URL")
    return parser.parse_args()

def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def ensure_readme_exists():
    if not os.path.exists(README_FILE):
        with open(README_FILE, "w") as f:
            f.write("| No  | Site | Title | Solution Link | Problem Link | Last Solve |\n")
            f.write("|-----|------|-------|----------------|--------------|-------------|\n")

def update_readme(site, title, filename, link, timestamp):
    ensure_readme_exists()
    number = filename.split("_")[1].split(".")[0]  # e.g., 001
    solution_link = f"[{filename}]({filename})"
    problem_link = f"[문제 링크]({link})"
    row = f"| {int(number)} | {site} | {title} | {solution_link} | {problem_link} | {timestamp} |\n"

    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_index = 2  # after the table header
    lines.insert(header_index, row)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

def git_commit_and_push(title):
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Add: {title}"], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    args = parse_arguments()
    timestamp = get_current_timestamp()

    update_readme(args.site, args.title, args.filename, args.link, timestamp)
    git_commit_and_push(args.title)
    print(f"✅ '{args.title}' 업로드 완료! README 갱신 및 GitHub 푸시 완료 🎉")

if __name__ == "__main__":
    main()
