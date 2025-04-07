# Import required libraries
import csv
import os
import sys
import argparse
from dotenv import load_dotenv
from .pubmed_parser import search_pubmed, fetch_details, parse_article
from .utils import print_info, print_success, print_error

def parse_args():

    # Parse command-line arguments.

    # Returns:
    # argparse.Namespace: Parsed arguments containing query, debug flag, and file name.

    parser = argparse.ArgumentParser(
        description="PubMed Research Paper Extractor",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="PubMed search query string (e.g., 'cancer AND immunotherapy')"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Print debug information during execution"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        default="pubmed_results.csv",
        help="Specify filename to save results"
    )
    return parser.parse_args()

    # Main execution function for extracting non-academic research papers from PubMed.

def main():
    args = parse_args()

     # Load API key from .env file

    load_dotenv()
    api_key = os.getenv("PUBMED_API_KEY")
    if not api_key:
        print_error("API key not found in .env file.")
        return

# Predefined queries (for convenience if query not passed)
    queries = {
        "1": "cancer AND immunotherapy",
        "2": "\"machine learning\" AND radiology",
        "3": "(covid-19 OR coronavirus) AND vaccine",
        "4": "CRISPR NOT bacteria",
        "5": "asthma[MeSH Terms] AND 2023[PDAT]"
    }

 # Get the query either from args or interactive input
    if args.query:
        query = args.query
    else:
        print_info("Select a PubMed query type:")
        for key, val in queries.items():
            print(f"{key}. {val}")
        choice = input("Enter option (1-5): ").strip()
        query = queries.get(choice)
        if not query:
            print_error("Invalid selection. Please choose a valid option.")
            return

    try:
        if args.debug:
            print_info(f"Using query: {query}")
            print_info(f"Saving results to: {args.file}")

        print_info("Searching PubMed...")
        pmids = search_pubmed(query, api_key, retmax=50)

        print_info(f"Fetching details for {len(pmids)} articles...")
        articles = fetch_details(pmids, api_key)

        results = []
        for article in articles:
            parsed = parse_article(article)
            if parsed:
                results.append(parsed)

        if not results:
            print_error("No articles found with non-academic authors.")
            return

       # Write the filtered results to CSV
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "PubmedID",
                "Title",
                "Publication Date",
                "Non-academicAuthor(s)",
                "CompanyAffiliation(s)",
                "Corresponding Author Email"
            ])
            writer.writeheader()
            writer.writerows(results)

        print_success(f"Success! Found {len(results)} articles. CSV saved as '{args.file}'.")
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

