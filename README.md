# PubMed Fetcher

Fetches PubMed articles with non-academic authors and exports details to CSV.

## Setup

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Run:

```bash
poetry install

##Run program
poetry run get-papers-list

OR

poetry run get-papers-list "CRISPR NOT bacteria" --f result.csv


##Result
Defualt it will fetch 50 results in 1 csv file if there are any

Result (csv file) will store in root folder as pubmed_result.csv

