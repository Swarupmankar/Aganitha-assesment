
import re
from rich import print

def is_non_academic_affiliation(affil):
    if affil is None:
        return False
    non_academic_keywords = ['inc', 'corp', 'ltd', 'gmbh', 'co.', 'company', 'llc', 'pharma', 'biotech', 'therapeutics']
    academic_keywords = ['university', 'institute', 'college', 'hospital', 'school', 'center', 'centre']
    affil = affil.lower()
    return any(k in affil for k in non_academic_keywords) and not any(k in affil for k in academic_keywords)

def extract_email(text):
    if text:
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return match.group(0) if match else ''
    return ''

def print_success(msg):
    print(f"[green]✔ {msg}[/green]")

def print_info(msg):
    print(f"[cyan]ℹ {msg}[/cyan]")

def print_error(msg):
    print(f"[red]✖ {msg}[/red]")