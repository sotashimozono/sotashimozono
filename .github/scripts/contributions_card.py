"""Draw profile/contributions.svg: projects outside my own accounts that carry my commits.

Styled to sit under the github-readme-stats cards (same colours, fonts and border).
"""

import json
import subprocess
import sys
from html import escape
from pathlib import Path

LOGIN = "sotashimozono"
OUTPUT = Path("profile/contributions.svg")
# My own organizations' repositories all sit below this, so the floor keeps them off the card
# without naming them.
MIN_STARS = 6
WIDTH = 771  # stats card (467) + languages card (300) + the gap GitHub renders between them
PADDING = 25
ROW_HEIGHT = 28
BACKGROUND, BORDER, TITLE, TEXT, MUTED = "#0d1117", "#ff79c6", "#ff79c6", "#bd93f9", "#8b949e"

REPOSITORIES = """
query($login: String!, $after: String) {
  user(login: $login) {
    repositoriesContributedTo(first: 100, after: $after, contributionTypes: [COMMIT],
                              includeUserRepositories: false, privacy: PUBLIC) {
      pageInfo { hasNextPage endCursor }
      nodes { nameWithOwner stargazerCount owner { login } }
    }
  }
}
"""


def gh(*args):
    return json.loads(subprocess.run(["gh", "api", *args], check=True, capture_output=True, text=True).stdout)


def contributed_repositories():
    repositories, after = [], None
    while True:
        args = ["graphql", "-f", f"query={REPOSITORIES}", "-f", f"login={LOGIN}"]
        if after:
            args += ["-f", f"after={after}"]
        page = gh(*args)["data"]["user"]["repositoriesContributedTo"]
        repositories += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            return repositories
        after = page["pageInfo"]["endCursor"]


def merged_pull_requests(repository):
    query = f"repo:{repository} is:pr is:merged author:{LOGIN}"
    return gh("-X", "GET", "search/issues", "-f", f"q={query}", "-f", "per_page=1")["total_count"]


def compact(number):
    return f"{number / 1000:.1f}k".replace(".0k", "k") if number >= 1000 else str(number)


def cell(x, y, width, entry):
    owner, name = entry["name"].split("/")
    merged = entry["merged"]
    detail = f"{merged} PR{'s' if merged != 1 else ''} · " if merged else ""
    return (
        f'<text x="{x}" y="{y}" class="name"><tspan class="owner">{escape(owner)}/</tspan>{escape(name)}</text>'
        f'<text x="{x + width}" y="{y}" class="detail" text-anchor="end">{detail}'
        f'<tspan class="star">★</tspan> {compact(entry["stars"])}</text>'
    )


def render(entries):
    rows = (len(entries) + 1) // 2
    height = 55 + rows * ROW_HEIGHT + PADDING - 10
    column = (WIDTH - 2 * PADDING - 40) // 2
    cells = []
    for index, entry in enumerate(entries):
        x = PADDING + (index % 2) * (column + 40)
        y = 72 + (index // 2) * ROW_HEIGHT
        cells.append(cell(x, y, column, entry))
    summary = ", ".join(entry["name"] for entry in entries)
    return f"""<svg width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="descId">
  <title id="titleId">Open source contributions</title>
  <desc id="descId">Projects with commits by {LOGIN}: {escape(summary)}</desc>
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {TITLE}; }}
    .name {{ font: 600 13px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif; fill: {TEXT}; }}
    .owner {{ font-weight: 400; fill: {MUTED}; }}
    .detail {{ font: 400 12px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif; fill: {MUTED}; }}
    .star {{ fill: {TITLE}; }}
  </style>
  <rect x="0.5" y="0.5" rx="4.5" width="{WIDTH - 1}" height="{height - 1}" fill="{BACKGROUND}" stroke="{BORDER}"/>
  <text x="{PADDING}" y="35" class="header">Open Source Contributions</text>
  {chr(10).join("  " + line for line in cells).strip()}
</svg>
"""


def main():
    entries = []
    for repository in contributed_repositories():
        if repository["owner"]["login"] == LOGIN or repository["stargazerCount"] < MIN_STARS:
            continue
        entries.append(
            {
                "name": repository["nameWithOwner"],
                "stars": repository["stargazerCount"],
                "merged": merged_pull_requests(repository["nameWithOwner"]),
            }
        )
    if not entries:
        sys.exit("no contributions found; refusing to write an empty card")
    entries.sort(key=lambda entry: (-entry["merged"], -entry["stars"]))
    OUTPUT.write_text(render(entries))
    print(f"wrote {OUTPUT} with {len(entries)} projects")


if __name__ == "__main__":
    main()
