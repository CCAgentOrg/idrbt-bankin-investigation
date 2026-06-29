#!/usr/bin/env python3
"""Fix remaining backslash-quotes in the raw string template only."""

FILE = '/home/workspace/idrbt-bankin-investigation/gen_site.py'

with open(FILE, 'r') as f:
    lines = f.readlines()

# Find the raw string template boundaries
# It starts with HTML = r""" and ends with the matching """
start = None
end = None
for i, line in enumerate(lines):
    if 'HTML = r"""' in line:
        start = i
    if start is not None and i > start and '"""' in line and not line.strip().startswith('#'):
        # This could be the closing. Check it has the pattern of template end
        stripped = line.strip()
        if stripped == '"""' or stripped == '"""' or stripped == '"""':
            end = i
            break
        # Also check for r"""" at end 
        if stripped.rstrip().endswith('"""') and not stripped.rstrip().endswith('r"""'):
            end = i
            break

if start is None or end is None:
    print(f"ERROR: Template boundaries not found. start={start}, end={end}")
    exit(1)

print(f"Template found: lines {start+1}-{end+1} (0-indexed: {start}-{end})")

# Count backslash-quote pairs in template section
count_before = 0
for line in lines[start:end+1]:
    count_before += line.count('\\"')

print(f"Backslash-quote pairs in template BEFORE: {count_before}")

# Fix: replace \" with a placeholder, then with just quote 
# In the raw string, \" is literally backslash-quote, should just be "
fixed_lines = []
for i, line in enumerate(lines):
    if start <= i <= end:
        line = line.replace('\\"', '"')
    fixed_lines.append(line)

count_after = 0
for line in fixed_lines[start:end+1]:
    count_after += line.count('\\"')

with open(FILE, 'w') as f:
    f.writelines(fixed_lines)

print(f"Backslash-quote pairs in template AFTER: {count_after}")
print(f"Fixed: {count_before - count_after} occurrences")
print("Now run gen_site.py to regenerate")
