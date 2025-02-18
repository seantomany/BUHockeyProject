import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import pandas as pd

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def scrape_website(url, delay=1, excel_output=None):
    if not is_valid_url(url):
        raise ValueError("Invalid URL format")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Add delay to prevent aggressive scraping
        time.sleep(delay)
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract tables and convert to DataFrames
        tables = soup.find_all('table')
        dataframes = []
        for table in tables:
            # Extract headers
            headers = []
            for th in table.find_all('th'):
                headers.append(th.text.strip())
            
            # If no headers found, use empty strings
            if not headers:
                headers = [f'Column_{i}' for i in range(len(table.find_all('tr')[0].find_all(['td', 'th'])))]
            
            # Extract rows
            rows = []
            for tr in table.find_all('tr'):
                row = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                if row and len(row) == len(headers):  # Only append rows that match header length
                    rows.append(row)
            
            if rows:
                df = pd.DataFrame(rows[1:] if headers in rows else rows, columns=headers)
                dataframes.append(df)
        
        # Get existing content
        paragraphs = soup.find_all('p')
        text_content = [p.text.strip() for p in paragraphs if p.text.strip()]
        links = soup.find_all('a')
        href_links = [link.get('href') for link in links if link.get('href')]
        
        # If excel_output is provided, save tables to Excel
        if excel_output and dataframes:
            with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
                for i, df in enumerate(dataframes):
                    sheet_name = f'Table_{i+1}'
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return {
            'text_content': text_content,
            'links': href_links,
            'status_code': response.status_code,
            'tables': dataframes
        }
        
    except requests.Timeout:
        raise TimeoutError("Request timed out")
    except requests.RequestException as e:
        raise RuntimeError(f"Scraping error: {str(e)}")

# Example usage
if __name__ == "__main__":
    website_url = "https://en.wikipedia.org/wiki/Boston_University_Terriers_men%27s_ice_hockey"  # Replace with your target website
    excel_file = "scraped_tables.xlsx"  # Name of the output Excel file
    
    try:
        result = scrape_website(website_url, excel_output=excel_file)
        print("Status Code:", result['status_code'])
        print(f"\nNumber of tables found: {len(result['tables'])}")
        print(f"Tables have been saved to '{excel_file}'")
        
        for i, df in enumerate(result['tables']):
            print(f"\nTable {i+1} Preview:")
            print(df.head())
        
    except Exception as e:
        print(f"Error: {e}")

