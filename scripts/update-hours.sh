#!/bin/bash

WORKLOG_FILE="documentation/WORKLOG.md"
README_FILE="README.md"

# Check if the WORKLOG.md file exists, if not, exit with an error
if [ ! -f "$WORKLOG_FILE" ]; then
  echo "Error: WORKLOG.md file not found!"
  exit 1
fi

# Extract total hours worked from WORKLOG.md
total_hours=0

# Use grep to find all "Hours Worked" occurrences and sum them correctly
grep -oP '\*\*Hours\ Worked\*\*:\s*\K\d+' "$WORKLOG_FILE" | while read -r hours; do
    total_hours=$((total_hours + hours))
done

# New fix: Allow for extra spaces before the number
grep -oP '\*\*Hours\ Worked\*\*:\s*\K\d+' "$WORKLOG_FILE" | while read -r hours; do
    total_hours=$((total_hours + hours))
done

echo "Total hours calculated: ${total_hours}"

# Python script to update the markdown files
update_files() {
    local file=$1
    local total_hours=$2

    python3 << EOF
import re

file_path = "$file"
total_hours = "$total_hours"

with open(file_path, 'r') as file:
    content = file.read()

# Update the line containing Total Hours Worked
content = re.sub(
    r"(!\[⏱️\]\(.*?\) \*\*Total Hours Worked\*\*: _)\s*([0-9]+ hours)\s*(_ \(Auto-generated\))",
    r"\g<1>{} hours\g<3>".format(total_hours),
    content
)

with open(file_path, 'w') as file:
    file.write(content)

print(f"Updated {file_path} successfully.")
EOF
}

# Ensure both WORKLOG.md and README.md are updated
update_files "$WORKLOG_FILE" "$total_hours"
if [ -f "$README_FILE" ]; then
    update_files "$README_FILE" "$total_hours"
else
    echo "Warning: README.md file not found!"
fi

echo "Script finished. Please verify changes."
