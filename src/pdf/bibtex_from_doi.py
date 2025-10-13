#!/usr/bin/env python3
import time
import sys
import requests
import pandas as pd
from urllib.parse import quote

# ------------ CONFIG ------------
INPUT_XLSX = "/home/pedro/Documents/git-repos/syst_review_tools/part4-analysed-with-doi-bibtex.xlsx"   # produced earlier
SHEET_NAME = "de_sheet_devel"                        # your target sheet
TITLE_COL_CANDIDATES = ["TITLE", "Title", "title", "Paper", "paper", "Name", "name"]
DOI_COL = "DOI"
OUT_TXT = "bibtex_all.txt"
UPDATE_EXCEL_BIBTEX = True                           # set to False to skip updating Excel
BIBTEX_COL = "BibTeX"
USER_AGENT = "INESC-TEC-bibtex-fetcher/1.0 (mailto:your.email@example.com)"  # please customize
REQUESTS_TIMEOUT = 25
MAX_RETRIES = 4
BACKOFF_BASE_SECS = 0.6
# --------------------------------

def find_title_col(df):
    for c in TITLE_COL_CANDIDATES:
        if c in df.columns:
            return c
    # fallback: first column
    return df.columns[0]

def fetch_bibtex_from_crossref(doi: str) -> str:
    """
    Use Crossref content negotiation (same output class as doi2bib).
    """
    # URL-encode the DOI (safe='') so slashes etc. stay safe
    url = f"https://api.crossref.org/works/{quote(doi, safe='')}/transform/application/x-bibtex"
    headers = {"User-Agent": USER_AGENT}
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=headers, timeout=REQUESTS_TIMEOUT)
            if r.status_code == 200:
                txt = r.text.strip()
                if txt and "@" in txt:   # quick sanity check for BibTeX
                    return txt
            # 429/5xx: backoff and retry
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(BACKOFF_BASE_SECS * (2 ** (attempt - 1)))
                continue
            # Other status codes: no point retrying
            break
        except Exception as e:
            last_exc = e
            time.sleep(BACKOFF_BASE_SECS * (2 ** (attempt - 1)))
    # If we got here, we failed to fetch a proper BibTeX
    if last_exc:
        sys.stderr.write(f"[warn] DOI {doi}: {last_exc}\n")
    else:
        sys.stderr.write(f"[warn] DOI {doi}: HTTP {r.status_code}\n")
    return ""

def minimal_bibtex(doi: str, title: str) -> str:
    """
    Generate a minimal, valid BibTeX without any f-string brace pitfalls.
    """
    key = doi.replace("/", "_")
    # Build with concatenation to avoid f-string/format brace escaping
    entry = (
        "@misc{" + key + ",\n"
        "  doi = {" + doi + "},\n"
        "  title = {" + (title or "Untitled") + "}\n"
        "}"
    )
    return entry

def main():
    df = pd.read_excel(INPUT_XLSX, sheet_name=SHEET_NAME)
    if DOI_COL not in df.columns:
        raise SystemExit(f"Column '{DOI_COL}' not found in sheet '{SHEET_NAME}'")

    title_col = find_title_col(df)
    dois = (
        df[DOI_COL]
        .astype(str)
        .str.strip()
        .replace({"": None, "nan": None})
        .dropna()
        .tolist()
    )

    # Preserve row order (not just unique) so your output aligns with the sheet order
    bib_list = []
    fetched_count = 0
    fallback_count = 0

    for i, row in df.iterrows():
        doi = str(row.get(DOI_COL, "")).strip()
        if not doi:
            bib_list.append("")  # keep position
            continue

        bib = fetch_bibtex_from_crossref(doi)
        if not bib:
            # fallback minimal
            bib = minimal_bibtex(doi, str(row.get(title_col, "")).strip())
            fallback_count += 1
        else:
            fetched_count += 1

        bib_list.append(bib)
        # gentle pacing to be polite to the API
        time.sleep(0.15)

    # Write all non-empty to txt (contiguous list)
    non_empty_bib = [b for b in bib_list if b]
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n\n".join(non_empty_bib))

    print(f"✅ Wrote {len(non_empty_bib)} entries to {OUT_TXT} "
          f"(fetched={fetched_count}, fallback={fallback_count})")

    # Optionally store back into Excel in a BibTeX column
    if UPDATE_EXCEL_BIBTEX:
        df[BIBTEX_COL] = bib_list
        df.to_excel(INPUT_XLSX, sheet_name=SHEET_NAME, index=False)
        print(f"✅ Updated column '{BIBTEX_COL}' in {INPUT_XLSX} (sheet '{SHEET_NAME}')")

if __name__ == "__main__":
    main()
