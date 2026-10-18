#!/usr/bin/env python3
"""Refresh the recent_pushes block in README.md with my most recently pushed repos.

Run by .github/workflows/update-readme.yml. Uses GITHUB_TOKEN when set (higher rate limit).
"""
import json
import os
import re
import urllib.request
from pathlib import Path

USER = "Karthik-099"
COUNT = 5
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- recent_pushes starts -->", "<!-- recent_pushes ends -->"


def fetch_repos():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed&type=owner",
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def line(repo):
    desc = (repo.get("description") or "").strip()
    if len(desc) > 80:
        desc = desc[:79].rstrip() + "…"
    desc = desc.replace("|", "\\|").replace("[", "(").replace("]", ")")
    text = f"- [{repo['name']}]({repo['html_url']})"
    if desc:
        text += f" — {desc}"
    return f"{text} · {repo['pushed_at'][:10]}"


def main():
    repos = [r for r in fetch_repos()
             if not r["fork"] and not r["archived"] and not r["private"] and r["name"] != USER]
    block = "\n".join(line(r) for r in repos[:COUNT])
    text = README.read_text(encoding="utf-8")
    new = re.sub(f"{re.escape(START)}.*?{re.escape(END)}", f"{START}\n\n{block}\n\n{END}", text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README updated")
    else:
        print("no change")


if __name__ == "__main__":
    main()
