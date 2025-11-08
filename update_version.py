import sys, re, datetime

if len(sys.argv) != 2:
    print("Usage: python update_version.py vX.Y.Z")
    sys.exit(1)

version = sys.argv[1].lstrip("v")
date = datetime.date.today().isoformat()

# --- Update README.md version badge ---
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

new_readme = re.sub(
    r"version-[\d\.]+-blue",
    f"version-{version}-blue",
    readme
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

# --- Append to CHANGELOG.md ---
entry = f"\n## [{version}] — {date}\n### Added\n- Describe new features here\n"

with open("CHANGELOG.md", "a", encoding="utf-8") as f:
    f.write(entry)

print(f"✅ Updated README and CHANGELOG for version {version}")
