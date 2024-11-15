import pandas as pd
import re
from rapidfuzz import fuzz

def match_customers_with_sanctions(customer_file_path, sanctions_file_path, name_threshold=80):
    # Regular expressions for free text parsing
    regex_patterns = {
        'name': r'(?i)name:\s*([a-zA-Z\s]+)',
        'dob': r'(?i)dob:\s*([\d/]+)',
        'country': r'(?i)country:\s*([a-zA-Z\s]+)',
        'id_number': r'(?i)(?:id number|passport|license):\s*([a-zA-Z\d]+)'
    }

    # Function to load data based on file format
    def load_data(file_path):
        # Determine format based on file extension
        if file_path.endswith('.csv') or file_path.endswith('.tsv'):
            delimiter = ',' if file_path.endswith('.csv') else '\t'
            return pd.read_csv(file_path, delimiter=delimiter)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:  # Assume free text if format is unknown
            return parse_free_text(file_path, regex_patterns)

    # Function to parse free text data
    def parse_free_text(file_path, regex_patterns):
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                entry = {field: re.search(pattern, line) for field, pattern in regex_patterns.items()}
                parsed_entry = {
                    'name': entry['name'].group(1).strip().lower() if entry['name'] else None,
                    'dob': entry['dob'].group(1).strip() if entry['dob'] else None,
                    'country': entry['country'].group(1).strip() if entry['country'] else None,
                    'id_number': entry['id_number'].group(1).strip().lower() if entry['id_number'] else None
                }
                data.append(parsed_entry)
        return pd.DataFrame(data)

    # Function for fuzzy matching, handling potential misspellings
    def fuzzy_match(row, sanctions_data, name_threshold):
        # Filter by dob and id_number
        potential_matches = sanctions_data[
            (sanctions_data['dob'] == row.get('dob')) |
            (sanctions_data['id_number'] == row.get('id_number'))
        ]
        
        # Apply fuzzy matching on name if available
        if row.get('name') and not potential_matches.empty:
            potential_matches['name_score'] = potential_matches['name'].apply(
                lambda x: fuzz.token_set_ratio(x, row['name']) if pd.notna(x) else 0
            )
            potential_matches = potential_matches[potential_matches['name_score'] >= name_threshold]
        
        return potential_matches

    # Load customer and sanctions data using the load_data function
    customer_data = load_data(customer_file_path)
    sanctions_data = load_data(sanctions_file_path)

    # Ensure columns are in lowercase to standardize
    customer_data.columns = customer_data.columns.str.lower()
    sanctions_data.columns = sanctions_data.columns.str.lower()

    # Apply fuzzy matching to each customer record
    matches = pd.concat(
        customer_data.apply(lambda row: fuzzy_match(row, sanctions_data, name_threshold), axis=1).tolist()
    ).dropna().reset_index(drop=True)

    return matches

# Example usage
customer_file_path = '/mnt/data/column_free_data.txt'
sanctions_file_path = '/mnt/data/sanctions_list.txt'
matches = match_customers_with_sanctions(customer_file_path, sanctions_file_path)
matches
