import argparse
import datetime
import os
import shutil
import subprocess

README_FILE = "README.md"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Upload solved problem to GitHub with README update.")
    parser.add_argument("--site", required=True, choices=["boj", "pgm"], help="boj or pgm")
    parser.add_argument("--title", required=True, help="Problem title")
    parser.add_argument("--filename", required=True, help="Filename (e.g., pgm_120802.c)")
    parser.add_argument("--link", required=True, help="Problem URL")
    return parser.parse_args()

def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def extract_problem_number(filename):
    base = os.path.basename(filename)
    try:
        return base.split("_")[1].split(".")[0]
    except IndexError:
        raise ValueError("파일 이름은 site_problemNumber.c 형식이어야 합니다. 예: pgm_120802.c")

def ensure_folder(site):
    if not os.path.exists(site):
        os.makedirs(site)

def move_file_to_site_folder(site, filename):
    ensure_folder(site)
    shutil.move(filename, os.path.join(site, filename))

def ensure_readme_exists():
    if not os.path.exists(README_FILE):
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write("| No     | Site | Title | Solution Link | Problem Link | Last Solve |\n")
            f.write("|--------|------|-------|----------------|--------------|-------------|\n")

def update_readme(site, title, filename, link, timestamp):
    ensure_readme_exists()
    problem_number = extract_problem_number(filename)
    file_path = f"{site}/{filename}"
    solution_link = f"[{filename}]({file_path})"
    problem_link = f"[문제 링크]({link})"
    new_row = f"| {problem_number} | {site} | {title} | {solution_link} | {problem_link} | {timestamp} |\n"

    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header = lines[:2]
    body = lines[2:]
    body.append(new_row)

    # 날짜 기준 내림차순 정렬 (마지막 열 기준)
    body.sort(key=lambda line: line.strip().split("|")[-2].strip(), reverse=True)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(header + body)

def git_commit_and_push(title):
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Add: {title}"], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    args = parse_arguments()
    timestamp = get_current_timestamp()

    move_file_to_site_folder(args.site, args.filename)
    update_readme(args.site, args.title, args.filename, args.link, timestamp)
    git_commit_and_push(args.title)
    print(f"\n✅ '{args.title}' 업로드 완료! 폴더 이동, README 정렬 및 GitHub 푸시 완료 🎉")

if __name__ == "__main__":
    main()
