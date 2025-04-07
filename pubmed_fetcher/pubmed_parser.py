# Import required libraries
import requests  # For making HTTP requests to the PubMed API
import xmltodict  # For parsing XML responses to Python dictionaries
from .utils import is_non_academic_affiliation, extract_email  # Custom utility functions

# Function to search for PubMed article IDs based on a query
def search_pubmed(query, api_key, retmax=20):
  
    # Searches PubMed using the given query and returns a list of PubMed IDs (PMIDs).

    # Parameters:
    #     query (str): Search query string.
    #     api_key (str): NCBI API key to authenticate and avoid request limits.
    #     retmax (int): Maximum number of results to return (default is 20).

    # Returns:
    #     List[str]: A list of PMIDs matching the query.

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"  # API endpoint for searching
    params = {
        "db": "pubmed",  # Specify the PubMed database
        "term": query,  # Search query
        "retmode": "json",  # Response format
        "retmax": retmax,  # Max number of results
        "api_key": api_key  # API key
    }

    res = requests.get(base_url, params=params)  # Make the GET request
    res.raise_for_status()  # Raise an exception if the request fails
    data = res.json()  # Parse the JSON response
    return data["esearchresult"]["idlist"]  # Return the list of article IDs (PMIDs)

# Function to fetch detailed metadata for a list of PMIDs
def fetch_details(pmids, api_key):
 
    # Fetches article metadata from PubMed for the given PMIDs.

    # Parameters:
    #     pmids (List[str]): List of PubMed IDs to fetch data for.
    #     api_key (str): NCBI API key.

    # Returns:
    #     List[dict]: A list of parsed XML article metadata in dictionary format.

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"  # Endpoint for fetching full article metadata
    params = {
        "db": "pubmed",  # Database
        "id": ",".join(pmids),  # Comma-separated string of PMIDs
        "retmode": "xml",  # Response format
        "api_key": api_key  # API key
    }

    res = requests.get(url, params=params)  # Make the request
    res.raise_for_status()  # Raise an exception on failure
    # Parse the XML response into a Python dictionary
    articles = xmltodict.parse(res.content)["PubmedArticleSet"]["PubmedArticle"]
    if isinstance(articles, dict):  # Ensure articles is a list, even if only one result
        articles = [articles]
    return articles

# Function to parse individual article metadata and extract relevant info
def parse_article(article):
   
    # Parses an individual article's metadata to extract:
    # - PubMed ID
    # - Title
    # - Publication Date
    # - Non-academic authors
    # - Affiliated companies
    # - Corresponding author email

    # Parameters:
    #     article (dict): Dictionary representing a single article’s metadata.

    # Returns:
    #     dict or None: Dictionary with extracted details if non-academic author found, else None.
    
    # Extract core metadata
    medline = article["MedlineCitation"]
    pmid = medline["PMID"]["#text"] if isinstance(medline["PMID"], dict) else medline["PMID"]

    # Extract article-level details
    article_data = medline.get("Article", {})
    title = article_data.get("ArticleTitle", "")

    # Try to get publication date from multiple possible fields
    pub_date = medline.get("DateCompleted") or article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
    date_str = "-".join([pub_date.get("Year", "0000"), pub_date.get("Month", "01"), pub_date.get("Day", "01")])

    # Extract the author list and normalize to a list
    authors = article_data.get("AuthorList", {}).get("Author", [])
    if isinstance(authors, dict):  # Handle case when only one author
        authors = [authors]

    # Prepare storage for non-academic authors, companies, and emails
    non_academic_authors = []
    companies = set()
    corresponding_email = ""

    # Loop through each author to analyze affiliation
    for author in authors:
        affiliation = ""
        if "AffiliationInfo" in author:
            aff_info = author["AffiliationInfo"]
            if isinstance(aff_info, list):  # Multiple affiliations
                affiliation = aff_info[0].get("Affiliation", "")
            else:  # Single affiliation
                affiliation = aff_info.get("Affiliation", "")

        # Check if the affiliation is non-academic (e.g., company)
        if is_non_academic_affiliation(affiliation):
            # Construct full name and store
            name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
            non_academic_authors.append(name)
            companies.add(affiliation)

        # Extract the email address from affiliation text (if not already found)
        if not corresponding_email:
            corresponding_email = extract_email(affiliation)

    # If no non-academic authors found, skip this article
    if not non_academic_authors:
        return None

    # Return structured result
    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": date_str,
        "Non-academicAuthor(s)": "; ".join(non_academic_authors),
        "CompanyAffiliation(s)": "; ".join(companies),
        "Corresponding Author Email": corresponding_email
    }
