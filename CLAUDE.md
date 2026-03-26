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
5. **Merge PDFs** — Activate the conda environment and run the merge script:
   ```
   conda activate .conda/
   python production/2_merge_frontpage.py
   ```
   This produces `production/production_output.pdf`.
6. **Rename and distribute** — Rename `production_output.pdf` to `YYYY-NN.pdf`, copy to `papers_backup/`, and upload to the USF economics website at `https://www.usf.edu/arts-sciences/departments/economics/documents/wpaper/YYYY-NN.pdf`.

## Naming Convention

Papers are numbered `YYYY-NN` where `YYYY` is the year and `NN` is a zero-padded sequential number within that year. The next number is determined by counting existing papers for the current year in `usfpaper.rdf` or `papers_backup/`.

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

# Merge front page with submission
conda activate .conda/
python production/2_merge_frontpage.py
```

## Dependencies

- **LaTeX**: pdfLaTeX with `graphicx`, `geometry`, `setspace`, `pdfpages`, `xcolor` packages
- **Python**: conda environment in `.conda/` with `PyPDF2`
