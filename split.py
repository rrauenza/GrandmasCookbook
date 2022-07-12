#!/usr/bin/python3

import re
from pathlib import Path
from collections import defaultdict

output = None

seen = set()

recipes = defaultdict(dict)

with open("export.txt") as fd:
    for line in fd.readlines():

        line = line.strip()
        line = re.sub(r' +', ' ', line)

        # print(line)

        if line == '_____':
            continue
        if line == '@@@@@':
            title = None
            category = None
            section = 0
            continue

        if line == '|':
            section += 1
            if section == 1:
                output.write("\n")
            if section == 2:
                output.write("\n### Ingredients\n\n")
            if section == 3:
                output.write("\n### Directions\n\n")
            continue

        if section == 0:
            if category is None:
                category = line
                continue
            if title is None:
                title = line
                Path(category).mkdir(parents=True, exist_ok=True)
                if title in seen:
                    assert False, f"Duplicate title: {title}"
                seen.add(title)
                filename = f"{category}/{title}.md"
                output = open(filename, "w")
                output.write(f"# {category}\n\n")
                output.write(f"## {title}\n")
                recipes[category][title] = filename
                continue
            assert False, f"{title}: There was another line in section 0: {line}"

        if section == 1:
            output.write(f"* {line}\n")

        if section == 2:
            output.write(f"* {line}\n")

        if section == 3:
            output.write(f"{line}\n")

        if section == 4:
            assert False, f"Section #{section}???"

if output:
    output.close()

with open("README.md", "w") as fd:
    fd.write("# Grandma's Recipes\n")
    for category in sorted(recipes.keys()):
        fd.write(f"## {category}\n")
        for title in sorted(recipes[category].keys()):
            filename = recipes[category][title]
            fd.write(f"* [{title}]({filename})\n")
