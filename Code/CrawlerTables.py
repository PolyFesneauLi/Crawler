import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin

# URL of the webpage to scrape
base_url = 'https://di.hkex.com.hk/di/NSAllSSList.aspx?sa2=as&sid=289810&corpn=Ocumension+Therapeutics+-+B&sd=01/07/2023&ed=31/12/2023&cid=0&sa1=cl&scsd=01%2f07%2f2023&sced=31%2f12%2f2023&sc=1477&src=MAIN&lang=EN&g_lang=en&'
base_domain = 'https://di.hkex.com.hk/di/'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to send HTTP request with retries
def fetch_url(url, headers, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL (attempt {i+1}/{retries}): {e}")
            time.sleep(random.uniform(1, 3))  # Add a random delay between retries
    return None

# Fetch the main URL
html_content = fetch_url(base_url, headers)
if html_content is None:
    print("Failed to fetch the main URL after multiple attempts.")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with id 'grdPaging'
table = soup.find('table', {'id': 'grdPaging'})

# Extract table headers
headers = []
h = table.find_all('tr')[0]
headers = [header.text.strip() for header in h.find_all('td')]

# Extract table rows
rows = []

for tr in table.find_all('tr')[1:]:  
    # the header row
    cells = tr.find_all('td')
    row = [cell.text.strip() for cell in cells]
    rows.append(row)
# Debug: Print headers and first row
print("Headers:", headers)
if rows:
    print("First row:", rows[0])
    print(rows.__len__())

# # Ensure the number of columns in headers matches the number of columns in rows
# if rows and len(headers) != len(rows[0]):
#     print(f"Warning: Number of headers ({len(headers)}) does not match number of columns in rows ({len(rows[0])}).")
#     # Adjust headers to match the number of columns in rows
#     headers = headers[:len(rows[0])]
#     print("Adjusted headers:", headers)


# Create a DataFrame
df = pd.DataFrame(rows, columns=headers)

# Save each table to a separate sheet in an Excel file
output_file = './output_SDI/Ocumension_Therapeutics.xlsx'
df.to_excel(output_file, index=False)
# with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
#     for idx, table in enumerate(tables):
#         sheet_name = f'Table_{idx + 1}'
#         table.to_excel(writer, sheet_name=sheet_name, index=False)

print(f'Data saved to {output_file}')