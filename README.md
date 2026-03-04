````markdown
# JSON → DOCX Project Exporter

Convert project records from a JSON file into a clean, CV-ready Word (DOCX) document. The pipeline reads JSON, groups and sorts projects, then exports styled DOCX files with bold titles, indented details, and consistent formatting.

## What you get
After running the scripts, these files will be generated:

- `AI_Projects.txt`
- `IoT_Projects.txt`
- `AI_Projects.docx`
- `IoT_Projects.docx`

## Requirements
- Python 3.8+
- Packages:
  - `python-docx`
  - `python-dateutil`

Install:
```bash
pip install python-docx python-dateutil
````

## Input format

The input file must be a JSON array stored as:

* `projectgrok.json`

Each project should include at least:

* `Project Title`
* `Project ID`
* `Start Date`
* `End Date`
* `My Role`
* `Classification` (`ai` or `iot`)
* `Funder/Sponsor` (optional)
* `Awarded Amount` (optional)
* `Institutes/Parties Involved` (optional)
* `Technology` (optional)

Dates are expected in: `D Month YYYY` (e.g., `1 September 2025`). Other formats will be left unchanged.

## How to run

Run the two scripts in order:

```bash
python cv-code.py
python toword.py
```

## How it works

1. `cv-code.py`

   * Reads `projectgrok.json`
   * Filters by `Classification`:

     * `ai` → `AI_Projects.txt`
     * `iot` → `IoT_Projects.txt`
   * Sorts projects by `Start Date` (newest first)
   * Outputs formatted Markdown-like text blocks

2. `toword.py`

   * Reads `AI_Projects.txt` and `IoT_Projects.txt`
   * Generates matching `.docx` files with:

     * Bold project titles
     * Indented details
     * Bold field keys (e.g., `Role:`, `Duration:`)
     * Consistent font and spacing

## Notes

* Classification matching is case-insensitive (`AI`, `ai`, `IoT`, `iot` all work).
* The scripts do not modify your original JSON content.
* If a project is missing a field, it will still be exported (blank values are allowed).

## Project structure (suggested)

```
.
├── projectgrok.json
├── cv-code.py
├── toword.py
├── AI_Projects.txt
├── IoT_Projects.txt
├── AI_Projects.docx
└── IoT_Projects.docx
```

```
```
