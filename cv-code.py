import json
from datetime import datetime
from dateutil.parser import parse

# -----------------------------------------------------------------------------
# Author Dr Shuo Ding, La Trobe Uni
# -----------------------------------------------------------------------------
# Read a JSON file ("projectgrok.json") that contains a list of project records,
# then:
#   1) Format each project into a short, human-readable Markdown snippet.
#   2) Split projects into two groups based on "Classification":
#        - "ai"  -> AI_Projects.txt
#        - "iot" -> IoT_Projects.txt
#   3) Sort each group by "Start Date" (newest first).
#   4) Write two output text files:
#        - AI_Projects.txt
#        - IoT_Projects.txt
#
# Notes:
# - This script does NOT modify project content; it only filters, sorts, and
#   formats.
# - Classification matching is case-insensitive (e.g., "AI", "ai", "Ai" all work).
# - Dates are formatted from "D Month YYYY" to "DD Mon YYYY" when possible.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Load project JSON data
# -----------------------------------------------------------------------------
# Expected input format: a JSON array of objects, e.g.:
# [
#   {"Project Title": "...", "Classification": "ai", "Start Date": "...", ...},
#   ...
# ]
with open("projectgrok.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------------------------------------------------------
# Date formatting helper
# -----------------------------------------------------------------------------
# Convert date strings from the expected input format:
#   "D Month YYYY"  (e.g., "1 September 2025")
# to:
#   "DD Mon YYYY"   (e.g., "01 Sep 2025")
#
# If parsing fails (unexpected date formats), return the original string.
def format_date(date_str: str) -> str:
    try:
        return datetime.strptime(date_str, "%d %B %Y").strftime("%d %b %Y")
    except Exception:
        return date_str

# -----------------------------------------------------------------------------
# Project formatting template
# -----------------------------------------------------------------------------
# Build a concise Markdown block for each project.
def format_project(p: dict) -> str:
    title = p.get("Project Title", "").strip()
    pid = p.get("Project ID", "")
    start = format_date(p.get("Start Date", ""))
    end = format_date(p.get("End Date", ""))
    role = p.get("My Role", "")
    funder = p.get("Funder/Sponsor", "")
    award = p.get("Awarded Amount", "")
    parties = p.get("Institutes/Parties Involved", "")
    tech = p.get("Technology", "")

    return (
        f"**{title}**  \n"
        f"Role: {role}  | Duration: {start} – {end}  | ID: {pid} \n"
        f"Sponsor: {funder} | Awarded Amount: {award} | Parties: {parties} | Key Tech: {tech}\n"
    )

# -----------------------------------------------------------------------------
# Sorting helper: parse Start Date for chronological sorting
# -----------------------------------------------------------------------------
# - If Start Date can be parsed, use it for sorting.
# - If it cannot be parsed, return datetime.min so those items fall to the end
#   when sorting newest-first (reverse=True).
def sort_key(p: dict) -> datetime:
    try:
        return parse(p.get("Start Date", ""), dayfirst=True)
    except Exception:
        return datetime.min

# -----------------------------------------------------------------------------
# Filter + sort by Classification (AI / IoT)
# -----------------------------------------------------------------------------
ai_projects = sorted(
    [x for x in data if x.get("Classification", "").lower() == "ai"],
    key=sort_key,
    reverse=True
)

iot_projects = sorted(
    [x for x in data if x.get("Classification", "").lower() == "iot"],
    key=sort_key,
    reverse=True
)

# -----------------------------------------------------------------------------
# Write output files
# -----------------------------------------------------------------------------
# Each project is written in Markdown format, followed by a blank line to keep
# the file readable.
with open("AI_Projects.txt", "w", encoding="utf-8") as f:
    for p in ai_projects:
        f.write(format_project(p) + "\n")

with open("IoT_Projects.txt", "w", encoding="utf-8") as f:
    for p in iot_projects:
        f.write(format_project(p) + "\n")

# -----------------------------------------------------------------------------
# Console output (echo)
# -----------------------------------------------------------------------------

print("✅ Done: projects filtered + sorted. Output files created: AI_Projects.txt and IoT_Projects.txt")
