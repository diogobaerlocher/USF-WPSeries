---
name: update-paper
description: Update an existing working paper in the USF Economics WP series. Regenerates the front page with an updated date, merges the new PDF, and updates the ReDIF metadata.
disable-model-invocation: true
argument-hint: [paper-number e.g. 2025-03] [path-to-new-pdf (optional)]
---

You are updating an existing paper in the USF Economics Working Paper Series.

## Step 0: Identify the paper

The paper number is `$0` (format: `YYYY-NN`). If not provided, ask the user.

Verify the paper exists by checking for its entry in `RePEc/usf/wpaper/usfpaper.rdf` and for `papers_backup/$0.pdf`. If not found, stop and tell the user.

## Step 1: Gather the updated PDF

If `$1` contains a path to a PDF, use it. Otherwise, check if `production/submission.pdf` exists and ask the user to confirm it is the updated version. If neither is available, ask the user to provide the path.

If a path was provided, copy it to `production/submission.pdf`.

## Step 2: Update the ReDIF entry

In `RePEc/usf/wpaper/usfpaper.rdf`, find the block for the paper (match on `Handle: RePEc:usf:wpaper:$0`).

Ask the user if any metadata needs updating (authors, title, abstract, JEL codes, keywords). If yes, apply the changes. If no, leave the existing metadata unchanged.

Regardless, update the `Creation-Date` field: keep the original date but add a `Revision-Date: YYYY-MM` line (current year-month) right after it. If a `Revision-Date` already exists, replace it with the current date.

## Step 3: Update the front page LaTeX

Read the current ReDIF entry for the paper to get title, abstract, authors, and affiliations.

Edit `production/1_create_frontpage.tex` with:
- Working Paper Number: `$0`
- Title, abstract, authors, and affiliations from the (possibly updated) ReDIF entry
- Availability date line should now read: `\noindent Available Online: ORIGINAL_MONTH ORIGINAL_YEAR | Updated: CURRENT_MONTH CURRENT_YEAR`
  - Derive `ORIGINAL_MONTH ORIGINAL_YEAR` from the `Creation-Date` field
  - Use the current date for the update

Important LaTeX considerations:
- Escape special characters: `&` -> `\&`, `%` -> `\%`, `$` -> `\$`, `#` -> `\#`
- Convert em-dashes (`—`) to `---`
- Convert en-dashes (`–`) to `--`
- Wrap words that should be italicized with `\textit{}`

## Step 4: Compile and merge

Run the following commands:
```bash
cd production && pdflatex 1_create_frontpage.tex && cd ..
conda activate .conda/ && python production/2_merge_frontpage.py
```

If pdflatex or python fails, show the error and stop.

## Step 5: Archive

Copy `production/production_output.pdf` to `papers_backup/$0.pdf`, replacing the previous version.

## Step 6: Summary

Print a checklist:
- [ ] ReDIF entry updated with `Revision-Date` in `RePEc/usf/wpaper/usfpaper.rdf`
- [ ] Front page recompiled with update date and merged into `production/production_output.pdf`
- [ ] Updated PDF saved to `papers_backup/$0.pdf`
- [ ] **Manual step**: Upload `papers_backup/$0.pdf` to the USF website at `documents/wpaper/$0.pdf`
- [ ] **Manual step**: Commit and push to GitHub so RePEc can crawl the updated RDF
