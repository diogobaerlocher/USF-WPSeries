---
name: add-paper
description: Add a new working paper to the USF Economics WP series. Handles ReDIF entry, front page, PDF merge, and numbering.
disable-model-invocation: true
argument-hint: [path-to-submission-pdf (optional)]
---

You are adding a new paper to the USF Economics Working Paper Series. Follow this pipeline exactly.

## Step 0: Gather inputs

If `$ARGUMENTS` contains a path to a PDF, use it as the submission file. Otherwise, check if `production/submission.pdf` already exists.

Ask the user to provide the filled-out submission form (the template is in `submission_form.txt`). Parse the following from it:
- All authors: full name, first name, last name, email, workplace, and optionally RePEc Short-ID (`Author-Person`)
- Title
- Abstract
- JEL codes (`Classification-JEL`)
- Keywords

If any required field is missing (authors, title, abstract), ask the user before proceeding.

## Step 1: Determine the paper number

Count how many papers already exist for the current year in `papers_backup/`. The new paper number is `YYYY-NN` where `NN` = (count + 1), zero-padded to two digits. Confirm the number with the user.

## Step 2: Create the ReDIF entry

Using `production/0_rdfCellTemplate.txt` as a structural reference, build a new ReDIF block with the collected metadata. The block must include:
- `Template-Type: ReDIF-Paper 1.0`
- All author fields (repeating the group for each co-author)
- `Title`, `Abstract`, `Classification-JEL`, `Keywords`
- `Creation-Date: YYYY-MM` (current year-month)
- `File-URL: https://www.usf.edu/arts-sciences/departments/economics/documents/wpaper/YYYY-NN.pdf`
- `File-Format: Application/pdf`
- `Number: YYYY-NN`
- `Handle: RePEc:usf:wpaper:YYYY-NN`

**Prepend** this block to `RePEc/usf/wpaper/usfpaper.rdf` (newest paper first), separated from the next entry by a blank line.

Also update `production/0_rdfCellTemplate.txt` with the new entry so it reflects the latest paper.

## Step 3: Update the front page LaTeX

Edit `production/1_create_frontpage.tex` with:
- Working Paper Number (line: `\noindent {\Large Working Paper Number YYYY-NN}`)
- Title (inside `\begin{center} \huge ... \end{center}`)
- Abstract (after `\noindent \textbf{Abstract:}`)
- Authors and affiliations (after `\noindent \textbf{Authors:}`) — first author on the `\noindent` line, subsequent authors on `\indent` lines, formatted as `Name, Affiliation \\`
- Availability date (line: `\noindent Available Online: Month YYYY`) — use the full month name

Important LaTeX considerations:
- Escape special characters: `&` -> `\&`, `%` -> `\%`, `$` -> `\$`, `#` -> `\#`
- Convert em-dashes (`—`) to `---`
- Convert en-dashes (`–`) to `--`
- Wrap words that should be italicized with `\textit{}`

## Step 4: Copy the submission PDF

If a PDF path was provided in the arguments, copy it to `production/submission.pdf`. If `production/submission.pdf` already exists and no path was given, confirm with the user that it is the correct file.

## Step 5: Compile and merge

Run the following commands:
```bash
cd production && pdflatex 1_create_frontpage.tex && cd ..
conda activate .conda/ && python production/2_merge_frontpage.py
```

If pdflatex or python fails, show the error and stop.

## Step 6: Rename and archive

Copy `production/production_output.pdf` to `papers_backup/YYYY-NN.pdf`.

## Step 7: Summary

Print a checklist:
- [ ] ReDIF entry added to `RePEc/usf/wpaper/usfpaper.rdf`
- [ ] Front page compiled and merged into `production/production_output.pdf`
- [ ] Final PDF saved to `papers_backup/YYYY-NN.pdf`
- [ ] **Manual step**: Upload `papers_backup/YYYY-NN.pdf` to the USF website at `documents/wpaper/YYYY-NN.pdf`
- [ ] **Manual step**: Commit and push to GitHub so RePEc can crawl the updated RDF
- [ ] **Optional**: Validate the ReDIF entry at https://econpapers.repec.org/scripts/redifcheck.pl
