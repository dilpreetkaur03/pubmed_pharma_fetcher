# PubMed Pharma Fetcher

Fetch PubMed research papers with at least one author affiliated with a pharmaceutical or biotech company, directly from the command line.

## Features

- Search PubMed using any query (supports full PubMed syntax)
- Filters for papers with non-academic (pharma/biotech) authors using smart heuristics
- Outputs results as a CSV file or a pretty table in the terminal
- Typed Python code, modular design, and robust error handling
- Easy to install and use via Poetry

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Install Poetry:**  
   [Poetry installation instructions](https://python-poetry.org/docs/#installation)

3. **Install dependencies:**
   ```sh
   poetry install
   ```

## Usage

### Basic search (prints to console)
```sh
poetry run get-papers-list "cancer immunotherapy"
```

### Save results to CSV
```sh
poetry run get-papers-list "cancer immunotherapy" -f results.csv
```

### Enable debug output
```sh
poetry run get-papers-list "cancer immunotherapy" -d
```

## How Non-Academic Authors Are Detected

- The tool uses heuristics to identify non-academic/company affiliations:
  - Looks for keywords (e.g., pharma, biotech, inc, ltd, corp, etc.) in author affiliations
  - Checks for company-like email domains
  - Excludes common academic keywords (university, department, etc.)

## Testing

Run all tests with:
```sh
poetry run pytest
```

## Project Structure

- `pubmed_pharma_fetcher/` — Main package (API, parser, heuristics, utils, models)
- `cli.py` — Command-line interface
- `tests/` — Unit and integration tests

## Dependencies

- requests
- typer
- pydantic
- rich
- pytest
- email-validator

## License

MIT License

---

*Built with ❤️ using Python and Poetry.*