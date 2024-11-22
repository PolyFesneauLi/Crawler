import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import pdfkit
from urllib.parse import urljoin

InputPath = './source/faf_documents.csv'
WritePath = './output_SDI'

# Base domain of the SDI URL
base_domain = 'https://di.hkex.com.hk/di/'

# Path to the wkhtmltopdf exe
path_to_wkhtmltopdf = r'G:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to send HTTP request with retries
# retries can be reset larger to guarantee the success of fetching the url
def fetch_url(url, headers, retries=10):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL (attempt {i+1}/{retries}): {e}")
            time.sleep(random.uniform(1, 3))  # Add a random delay between retries
    return None

def crawler_table(url,domain,headers) -> pd.DataFrame:
    html_content = fetch_url(url, headers)
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
    
    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # create new column fetch the sub link of serial number and and it to new column 'link'
    # first find serial number of a row
    # then find the link of the serial number and add it to the new column 'link'
    links = table.find_all('a')

    ''' debuger for links
    print(links.__len__())
    for i in range(links.__len__()):
        print(i,end='】 ')
        print(links[i].text )
    # print(type(links[0].text))
    for i in range(df['Form Serial Number'].__len__()):
        print(i,end='】 ')
        print(df['Form Serial Number'][i])
    '''
    
    '''debugger 00806
    base_url = https://di.hkex.com.hk/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/07/2023&sced=31/12/2023&sc=806&src=MAIN&lang=EN&g_lang=en
    print(type(df['Form Serial Number'][0]))
    print("【"*20)
    print(df['Form Serial Number'][0])
    # extraxt number series before '('
    t = df['Form Serial Number'][0].split('(')[0]
    t = t.split('(')[0]
    print(t)
    print("】"*20)
    '''
    df['link'] = [urljoin(domain, next(link['href'] for link in links if  df['Form Serial Number'][0].split('(')[0] in link.text)) for i in range(df['Form Serial Number'].__len__())]

    return df
    '''
    # # Save each table to a separate Excel files
    # output_file = f'{output_path}/{table_name}.xlsx'
    # df.to_excel(output_file, index=False)
    # print("【"f'Data saved to {output_file}'"】")
    '''

# get col 3 (SDI) of every row
def get_SDI(csvfile)->list:
    df = pd.read_csv(csvfile)
    return df['SDI'].tolist()

def save_webpage_to_pdf(url, output_path,config):
    try:
        pdfkit.from_url(url, output_path,configuration=config)
        print(f"Web page saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def FetchInfoForSDI(url,domain,headers,WritePath):
     # Fetch the main URL
    html_content = fetch_url(url, headers)
    if html_content is None:
        print("Failed to fetch the main URL after multiple attempts.")
        exit()

    '''
    # # Load local HTML file
    # with open('Hong Kong Exchanges and Clearing Limited.html', 'r', encoding='utf-8') as f:
    #     html_content = f.read()
    '''
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the table data where the links are located
    table = soup.find('table', id='grdPaging')

    # Initialize lists to store the extracted data
    stock_code = ''
    stock_name = ''
    Date_value = ''
    report_links = ''

    # Loop through the rows in the table to extract links
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        cells = row.find_all('td') # Extract the cells in each row

        stock_code = cells[0].text.strip()
        stock_name = cells[1].text.strip()

        # get date information
        Date_label = soup.find('td', string='Date (dd/mm/yyyy):')
        if Date_label:
            Date_value = Date_label.find_next_sibling('td').text.strip()

        '''
        # Extract the report links
        report_links.append({
            ## 优化一下，这边查找Complete list of substantial shareholders 后面跟的子链接,不是直接找a标签
            "Complete list of substantial shareholders": cells[2].find_all('a')[0]['href'],
            "Consolidated list of substantial shareholders": cells[2].find_all('a')[1]['href'],
            "List of notices filed by substantial shareholders": cells[2].find_all('a')[2]['href'],
            "Complete list of directors": cells[2].find_all('a')[3]['href'],
            "List of notices filed by directors": cells[2].find_all('a')[4]['href'],
            "List of all notices": cells[2].find_all('a')[5]['href'],
        })
        '''

        # Extract the report links
        links = cells[2].find_all('a')
        report_links = {
            "Complete list of substantial shareholders": urljoin(domain, next(link['href'] for link in links if "Complete list of substantial shareholders" in link.text)),
            "Consolidated list of substantial shareholders": urljoin(domain, next(link['href'] for link in links if "Consolidated list of substantial shareholders" in link.text)),
            "List of notices filed by substantial shareholders": urljoin(domain, next(link['href'] for link in links if "List of notices filed by substantial shareholders" in link.text)),
            "Complete list of directors": urljoin(domain, next(link['href'] for link in links if "Complete list of directors" in link.text)),
            "List of notices filed by directors": urljoin(domain, next(link['href'] for link in links if "List of notices filed by directors" in link.text)),
            "List of all notices": urljoin(domain, next(link['href'] for link in links if "List of all notices" in link.text)),
        }

        # Create a DataFrame
        data = {
        "Stock Code": stock_code,
        "Company Name": stock_name,
        "Date(dd/mm/yyyy)": Date_value,
        "Complete list of substantial shareholders": [report_links["Complete list of substantial shareholders"]],
        "Consolidated list of substantial shareholders": [report_links["Consolidated list of substantial shareholders"]],
        "List of notices filed by substantial shareholders": [report_links["List of notices filed by substantial shareholders"]],
        "Complete list of directors": [report_links["Complete list of directors"]],
        "List of notices filed by directors": [report_links["List of notices filed by directors"]],
        "List of all notices": [report_links["List of all notices"]],
    }
        df = pd.DataFrame(data)

        # Create a directory to save the Excel file
        
        # standardize the company name to remove special characters
        # only numbers letters and _ are allowed
        # change space to _
        stock_name = ''.join(e for e in stock_name if e.isalnum() or e == ' ').replace(' ', '_')
        stock_number = stock_code

        directory = f'{WritePath}/{stock_number}/({stock_number}){stock_name}'
        os.makedirs(directory, exist_ok=True)

        # Save DataFrame to Excel
        output_file = f'{directory}/Outline.xlsx'
        df.to_excel(output_file, index=False)

        print(f'Data saved to {output_file}')
        print('-' * 100)

        # Crawl the tables
        Combined_file = f'{directory}/Combined.xlsx'
        # new a empty file under {directory}/Combined.xlsx
        combined_file = os.path.join(directory, 'Combined.xlsx')
        # Create an empty DataFrame
        df_empty = pd.DataFrame()
        # Save the empty DataFrame to the Excel file
        df_empty.to_excel(combined_file, index=False)


        with pd.ExcelWriter(Combined_file, engine='openpyxl', mode='a') as writer:
            if 'Sheet1' in writer.book.sheetnames:
                        # Remove the existing sheet
                        del writer.book['Sheet1']
            # write outline.xlsx to Combined.xlsx
            if 'Outline' in writer.book.sheetnames:
                        # Remove the existing sheet
                        del writer.book['Outline']
            df.to_excel(writer, sheet_name='outline',index=False)
            for key, value in report_links.items():
                if value:
                    key = ''.join(e for e in key if e.isalnum() or e == ' ').replace(' ', '_')
                    key_for_sheet = key[:31]  ## no more than 31 characters
                    df = crawler_table(value,domain,headers)
                    #separate the tables into different files
                    output_path = f'{directory}/{key}'
                    ''' debuger for output_path.xlsx join or +
                    print('【'*20)
                    print(output_path)
                    print('】'*20)
                    print(output_path+('.xlsx'))
                    print('】'*20)
                    '''
                    df.to_excel(output_path+('.xlsx'), index=False)
                    # debuger for output_path
                    # print("【"f'Table {key} saved to {directory}/{key}.xlsx'"】")

                    # create folder as output_path
                    os.makedirs(output_path, exist_ok=True) # exist_ok=True means no error if the folder already exists
                    # store the  page of sub web link of serial number as pdf
                    for i in range(df['Form Serial Number'].__len__()):
                        print("【" + str(i) + "】")
                        sub_output_path = f'{output_path}/{df["Form Serial Number"][i]}.pdf'
                        # store web page of url to pdf
                        # we need to config the path of wkhtmltopdf
                        save_webpage_to_pdf(df['link'][i],sub_output_path,config)
                        print("【"f'Table {key} saved to {sub_output_path}'"】")

                    #combine all tables into one file
                    if key_for_sheet in writer.book.sheetnames:
                        # Remove the existing sheet
                        del writer.book[key_for_sheet]
                    df.to_excel(writer, sheet_name=key_for_sheet, index=False)
                    # debuger for Combined_file
                    # print("【"f'Table {key} saved to {Combined_file}'"】")    

# debugger URL of the webpage to scrape
# base_url = 'https://di.hkex.com.hk/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/07/2023&sced=31/12/2023&sc=1398&src=MAIN&lang=EN&g_lang=en'
# 00806
# base_url = 'https://di.hkex.com.hk/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/07/2023&sced=31/12/2023&sc=806&src=MAIN&lang=EN&g_lang=en'

SDIs = get_SDI(InputPath)
for SDI in SDIs:
    FetchInfoForSDI(SDI,base_domain,headers,WritePath)

# debuger for special url  
#FetchInfoForSDI(base_url,base_domain,headers,WritePath)

'''
# Fetch the main URL
html_content = fetch_url(base_url, headers)
if html_content is None:
    print("Failed to fetch the main URL after multiple attempts.")
    exit()

# # Load local HTML file
# with open('Hong Kong Exchanges and Clearing Limited.html', 'r', encoding='utf-8') as f:
#     html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract the table data where the links are located
table = soup.find('table', id='grdPaging')

# Initialize lists to store the extracted data
stock_code = []
company_name = []
Date_value = []
report_links = []

# Loop through the rows in the table to extract links
rows = table.find_all('tr')[1:]  # Skip the header row
for row in rows:
    cells = row.find_all('td') # Extract the cells in each row
    
    stock_code.append(cells[0].text.strip())
    company_name.append(cells[1].text.strip())
    
    # get date information
    Date_label = soup.find('td', string='Date (dd/mm/yyyy):')
    if Date_label:
        Date_value.append(Date_label.find_next_sibling('td').text.strip())
    
    # # Extract the report links
    # report_links.append({
    #     ## 优化一下，这边查找Complete list of substantial shareholders 后面跟的子链接，不是直接找a标签
    #     "Complete list of substantial shareholders": cells[2].find_all('a')[0]['href'],
    #     "Consolidated list of substantial shareholders": cells[2].find_all('a')[1]['href'],
    #     "List of notices filed by substantial shareholders": cells[2].find_all('a')[2]['href'],
    #     "Complete list of directors": cells[2].find_all('a')[3]['href'],
    #     "List of notices filed by directors": cells[2].find_all('a')[4]['href'],
    #     "List of all notices": cells[2].find_all('a')[5]['href'],
    # })

    # Extract the report links
    links = cells[2].find_all('a')
    report_links.append({
        "Complete list of substantial shareholders": urljoin(base_domain, next(link['href'] for link in links if "Complete list of substantial shareholders" in link.text)),
        "Consolidated list of substantial shareholders": urljoin(base_domain, next(link['href'] for link in links if "Consolidated list of substantial shareholders" in link.text)),
        "List of notices filed by substantial shareholders": urljoin(base_domain, next(link['href'] for link in links if "List of notices filed by substantial shareholders" in link.text)),
        "Complete list of directors": urljoin(base_domain, next(link['href'] for link in links if "Complete list of directors" in link.text)),
        "List of notices filed by directors": urljoin(base_domain, next(link['href'] for link in links if "List of notices filed by directors" in link.text)),
        "List of all notices": urljoin(base_domain, next(link['href'] for link in links if "List of all notices" in link.text)),
    })

# Create a DataFrame
data = {
    "Stock Code": stock_code,
    "Company Name": company_name,
    "Date(dd/mm/yyyy)": Date_value,
    "Complete list of substantial shareholders": [link["Complete list of substantial shareholders"] for link in report_links],
    "Consolidated list of substantial shareholders": [link["Consolidated list of substantial shareholders"] for link in report_links],
    "List of notices filed by substantial shareholders": [link["List of notices filed by substantial shareholders"] for link in report_links],
    "Complete list of directors": [link["Complete list of directors"] for link in report_links],
    "List of notices filed by directors": [link["List of notices filed by directors"] for link in report_links],
    "List of all notices": [link["List of all notices"] for link in report_links],
}
df = pd.DataFrame(data)

# Create a directory to save the Excel file
stock_name = company_name[0]
# standardize the company name to remove special characters
# only numbers letters and _ are allowed
# change space to _
stock_name = ''.join(e for e in stock_name if e.isalnum() or e == ' ').replace(' ', '_')
stock_number = stock_code[0]
directory = f'./output_SDI/{stock_name}({stock_number})'
os.makedirs(directory, exist_ok=True)

# Save DataFrame to Excel
output_file = f'{directory}/Outline.xlsx'
df.to_excel(output_file, index=False)

print(f'Data saved to {output_file}')
print('-' * 50)

# Crawl the tables
Combined_file = f'{directory}/Combined.xlsx'
# new a empty file under {directory}/Combined.xlsx
combined_file = os.path.join(directory, 'Combined.xlsx')
# Create an empty DataFrame
df_empty = pd.DataFrame()
# Save the empty DataFrame to the Excel file
df_empty.to_excel(combined_file, index=False)


with pd.ExcelWriter(Combined_file, engine='openpyxl', mode='a') as writer:
    if 'Sheet1' in writer.book.sheetnames:
                    # Remove the existing sheet
                    del writer.book['Sheet1']
    # write outline.xlsx to Combined.xlsx
    if 'Outline' in writer.book.sheetnames:
                    # Remove the existing sheet
                    del writer.book['Outline']
    df.to_excel(writer, sheet_name='outline',index=False)
    for i, link in enumerate(report_links):
        for key, value in link.items():
            if value:
                key = ''.join(e for e in key if e.isalnum() or e == ' ').replace(' ', '_')
                key_for_sheet = key[:31]  ## no more than 31 characters
                df = crawler_table(value,headers)
                #separate the tables into different files
                output_file = f'{directory}/{key}.xlsx'
                df.to_excel(output_file, index=False)
                print("【"f'Table {key} saved to {directory}/{key}.xlsx'"】")

                #combine all tables into one file
                if key_for_sheet in writer.book.sheetnames:
                    # Remove the existing sheet
                    del writer.book[key_for_sheet]
                df.to_excel(writer, sheet_name=key_for_sheet, index=False)
                print("【"f'Table {key} saved to {Combined_file}'"】")
'''         


