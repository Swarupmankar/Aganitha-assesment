# 🧬 PubMed Fetcher

A Python-based command-line tool to fetch and export PubMed research articles involving **non-academic authors** (e.g., from biotech or pharmaceutical companies). The results are parsed and saved into a CSV file with important metadata including affiliations and corresponding author details.

---

## 📁 Project Structure

```
pubmed-fetcher/
├── pubmed_exporter/
│   ├── __init__.py
│   ├── fetcher.py         # Handles PubMed API requests
│   └── parser.py          # Extracts and filters metadata
├── main.py                # CLI entry point
├── .env                   # API Key file (excluded from version control)
├── pyproject.toml         # Poetry project & dependency configuration
└── README.md              # Project documentation
```

---

## ⚙️ Features

- Supports full PubMed query syntax (e.g., `"CRISPR NOT bacteria"`).
- Extracts:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Authors
  - Company Affiliations
  - Corresponding Author Email
- Outputs results to a clean CSV file.
- Uses `Poetry` for virtual environment and dependency management.

---

## 🛠️ Installation

### Step 1: Install Poetry

Follow official instructions here:  
👉 [Poetry Installation Guide](https://python-poetry.org/docs/#installation)

### Step 2: Install Dependencies

Clone the repository and run:

```bash
poetry install
```

Make sure to add your PubMed API key to a `.env` file in the root directory:

```
NCBI_API_KEY=your_actual_api_key_here
```

---

## 🚀 Running the Program

### Basic usage:

```bash
poetry run get-papers-list
```

This will use the default query (`cancer AND biotech`) and fetch articles.

### Custom query and output:

```bash
poetry run get-papers-list "CRISPR NOT bacteria" --f result.csv

or

poetry run get-papers-list
```

- `--f` or `--outfile` lets you specify the output file name.
- The default result file is saved as `pubmed_result.csv` in the root folder.

---

## 🧰 Tools & Libraries Used

| Tool / Library | Description                              |
| -------------- | ---------------------------------------- |
| **Poetry**     | Dependency and packaging manager         |
| **requests**   | For making HTTP requests to PubMed API   |
| **xmltodict**  | XML to Python dictionary converter       |
| **pandas**     | For tabular data handling and CSV export |
| **dotenv**     | To load API keys from `.env` files       |
| **tqdm**       | For progress bars in CLI                 |

---

## 🧠 Author

**Swarup Mankar**  
For inquiries or improvements, feel free to reach out or submit a pull request.
