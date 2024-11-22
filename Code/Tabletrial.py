# # use pymupdf to open a pdf file
# # use Page.find_tables() to extract tables in the document 
# import fitz,sys,csv  # PyMuPDF

# # # Open the PDF file
# # fpath = sys.argv[1]
# # pdf_document = fitz.open(fpath)

# # # Iterate through each page
# # for page_num in range(len(pdf_document)):
# #     page = pdf_document.load_page(page_num)
    
# #     # Extract tables from the page
# #     tables = page.find_tables()
    
# #     # Print or process the extracted tables
# #     for table in tables:
# #         print(f"Table found on page {page_num + 1}:")
# #         # for row in table:
# #         #     print(row)

# # Open the PDF file
# fpath = sys.argv[1]
# pdf_document = fitz.open(fpath)

# # Open a CSV file to write the tables
# with open("extracted_tables.csv", mode="w", newline="") as csv_file:
#     csv_writer = csv.writer(csv_file)
    
#     # Iterate through each page
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
        
#         # Extract tables from the page
#         tables = page.find_tables()
        
#         # Process and write the extracted tables to the CSV file
#         for table in tables:
#             csv_writer.writerow([f"Table found on page {page_num + 1}:"])
#             for row in table:
#                 csv_writer.writerow([cell[4] for cell in row])
#             csv_writer.writerow([])  # Add an empty row between tables



# import fitz  # PyMuPDF
# import tabula
# import pandas as pd
# import sys
# import csv

# # Load your PDF
# pdf_path = sys.argv[1]
# # csv_path = sys.argv[2]

# # Extract tables using tabula-py
# tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

# # Save tables as CSV
# for i, table in enumerate(tables):
#     csv_path = f'table_{i + 1}.csv'
#     table.to_pandas.to_csv(csv_path, index=False, encoding='utf-8-sig')
#     print(f'Table {i + 1} saved to {csv_path}')


# scan every page and all possible tables
# 表的存在都能检测，但是解析效果很差，大单元格会被拆分 导致错位

import fitz  # PyMuPDF
import pandas as pd
import sys
import re

if not hasattr(fitz.Page, "find_tables"):
    raise RuntimeError("This PyMuPDF version does not support the table feature")

# Function to sanitize file names
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\n]', '_', name)

# Open the PDF file
pdf_path = sys.argv[1]
csv_path = "./output_tables/"
doc = fitz.open(pdf_path)

# Iterate through each page
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    
    # Extract tables from the page
    tables = page.find_tables()
    
    # Process and write the extracted tables to the CSV file
    for i, table in enumerate(tables):
        # Convert the table to a DataFrame
        df = table.to_pandas()
        
        header_names = "_".join([sanitize_filename(name) for name in table.header.names])

        # Save the DataFrame to a CSV file with UTF-8-SIG encoding
        output_csv_path = f"{csv_path}_page_{page_num + 1}_table_{i + 1}_{header_names}.csv"
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print(f"Table {i + 1} on page {page_num + 1} saved to {output_csv_path}")