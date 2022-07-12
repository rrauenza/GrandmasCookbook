#!/usr/bin/python3

from pathlib import Path

output = None

seen = set()

with open("export.txt") as fd:
    for line in fd.readlines():

        line = line.strip()

        print(line)

        if line == '@@@@@':
            title = None
            category = None
            section = 0
            continue

        if line == '|':
            section += 1

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
                output = open(f"{category}/{title}.md", "w")
                output.write(f"# {category}\n")
                output.write(f"## {title}\n")
                continue
            assert False, f"{title}: There was another line in section 0: {line}"


if output:
    output.close()
