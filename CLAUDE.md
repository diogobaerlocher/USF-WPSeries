# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

This is the USF Department of Economics Working Paper Series repository. It serves two purposes:
1. **RePEc integration** — The `RePEc/` directory is served via GitHub Pages so that RePEc crawlers can index paper metadata nightly.
2. **Front-page production** — The `production/` pipeline generates a branded cover page and merges it with the submitted PDF.

## Repository Structure

- `RePEc/usf/wpaper/usfpaper.rdf` — The main ReDIF metadata file. New papers are **prepended** (newest first). Each entry is a `Template-Type: ReDIF-Paper 1.0` block.
- `RePEc/usf/usfarch.rdf` / `usfseri.rdf` — Archive and series metadata (rarely changed).
- `production/` — The production pipeline (see below).
- `papers_backup/` — Local archive of final PDFs, named `YYYY-NN.pdf`.
- `submission_form.txt` — Template sent to authors to collect metadata.
- `.github/workflows/workflow.yml` — Deploys a directory listing to GitHub Pages on push (serves the RePEc directory).

## Production Pipeline

The workflow to add a new working paper:

1. **Collect metadata** via `submission_form.txt`.
2. **Create ReDIF entry** — Use `production/0_rdfCellTemplate.txt` as a template. Fill in author fields, title, abstract, JEL codes, keywords, `Creation-Date` (YYYY-MM), `Number` (YYYY-NN), `File-URL`, and `Handle`. Prepend the completed block to `RePEc/usf/wpaper/usfpaper.rdf`.
3. **Save submitted PDF** as `production/submission.pdf`.
4. **Edit the front page** — Update `production/1_create_frontpage.tex` with the paper number, title, abstract, authors + affiliations, and availability date. Then compile with pdfLaTeX.
5. **Merge PDFs** — Run the merge script through the project's virtual environment:
   ```
   # macOS / Linux
   .venv/bin/python production/2_merge_frontpage.py
   # Windows
   .venv\Scripts\python production\2_merge_frontpage.py
   ```
   This produces `production/production_output.pdf`.
6. **Rename and distribute** — Rename `production_output.pdf` to `YYYY-NN.pdf`, copy to `papers_backup/`, and upload to the USF economics website at `https://www.usf.edu/arts-sciences/departments/economics/documents/wpaper/YYYY-NN.pdf`.

## Naming Convention

Papers are numbered `YYYY-NN` where `YYYY` is the year and `NN` is a zero-padded sequential number within that year. The next number is determined by counting existing papers for the current year in `usfpaper.rdf` or `papers_backup/`.

## Copyright Block on the Front Page

The front page (`production/1_create_frontpage.tex`) has two variants of the bottom copyright block. Pick the one that matches the paper's publication status:

1. **Pre-print / initial release** — Default "All rights reserved" notice:
   ```latex
   \noindent \small ©The authors listed. All rights reserved. No part of this paper may be reproduced in any form, or stored in a retrieval system, without the prior written permission of the authors.
   ```

2. **Accepted-manuscript update** — When re-releasing the WP as the accepted version of a published article, switch to the CC BY-NC-ND 4.0 notice with journal citation and DOI. Requires `\usepackage{url}` (or `hyperref`) in the preamble:
   ```latex
   {\small
   \textcopyright{} The authors listed. This is the accepted manuscript version of an article accepted for publication
   in the \emph{Journal Name}. The version of record is available at
   \url{https://doi.org/<DOI>}. This work is licensed under a Creative Commons
   Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).
   \url{https://creativecommons.org/licenses/by-nc-nd/4.0/}
   }
   ```
   When using variant 2, also update the front page's "Updated: MONTH YEAR" line and add a matching `Revision-Date: YYYY-MM` to the paper's ReDIF block in `usfpaper.rdf`.

## ReDIF Format Notes

- Each paper block starts with `Template-Type: ReDIF-Paper 1.0` and ends with a blank line.
- `Handle: RePEc:usf:wpaper:YYYY-NN` must be unique.
- `File-URL` must point to the USF website PDF location.
- Author fields repeat for each co-author: `Author-Name`, `Author-Name-First`, `Author-Name-Last`, `Author-Email`, `Author-Workplace-Name`, and optionally `Author-Person` (RePEc Short-ID).
- Validate entries at: https://econpapers.repec.org/scripts/redifcheck.pl

## Key Commands

```bash
# Compile front page (from repo root)
cd production && pdflatex 1_create_frontpage.tex && cd ..

# Merge front page with submission (uses the project's venv)
.venv/bin/python production/2_merge_frontpage.py        # macOS / Linux
.venv\Scripts\python production\2_merge_frontpage.py    # Windows
```

## Commit Conventions

Do not add Claude as a co-author on commits. No `Co-Authored-By: Claude ...` trailer, no "Generated with Claude Code" line in the message body.

## Dependencies

- **LaTeX**: pdfLaTeX with `graphicx`, `geometry`, `setspace`, `pdfpages`, `xcolor`, `url` packages (install missing ones via `tlmgr install <pkg>`)
- **Python**: virtual environment in `.venv/` with `PyPDF2`. Create with `python3 -m venv .venv && .venv/bin/pip install PyPDF2` (macOS/Linux) or `py -m venv .venv && .venv\Scripts\pip install PyPDF2` (Windows). The `.venv/` folder is platform-specific — recreate it on each machine rather than syncing across Box.
