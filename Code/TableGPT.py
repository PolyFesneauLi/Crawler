# import fitz  # PyMuPDF
# import pandas as pd

# def extract_table_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     page = doc[0]
    
#     if not hasattr(fitz.Page, "find_tables"):
#         raise RuntimeError("This PyMuPDF version does not support the table feature")
    
#     tabs = page.find_tables()  # detect the tables
    
#     if not tabs:
#         print("No tables found!")
#         return None
    
#     # Choose the first table for this example
#     table = tabs[0]
    
#     # Convert the table to a Pandas DataFrame
#     df = table.to_pandas()
    
#     return df

# def save_table_to_files(df, excel_path, csv_path):
#     # Save to Excel
#     df.to_excel(excel_path, index=False)
#     print(f"Table saved to {excel_path}")
    
#     # Save to CSV
#     df.to_csv(csv_path, index=False, encoding='utf-8-sig')
#     print(f"Table saved to {csv_path}")



# # Paths to your files
# pdf_path = "../examplepdf/2.pdf"  # Replace with your actual PDF path
# excel_path = "output_table.xlsx"
# csv_path = "output_table.csv"

# # Extract the table
# df = extract_table_from_pdf(pdf_path)

# if df is not None:
#     # Save the table to both Excel and CSV files
#     save_table_to_files(df, excel_path, csv_path)

import fitz  # PyMuPDF
import pandas as pd
import re
import os

def extract_tables_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_tables = []
    
    if not hasattr(fitz.Page, "find_tables"):
        raise RuntimeError("This PyMuPDF version does not support the table feature")
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        tabs = page.find_tables()  # detect the tables
        
        if not tabs:
            print(f"No tables found on page {page_num + 1}")
            continue
        
        for i, table in enumerate(tabs):
            df = table.to_pandas()
            all_tables.append((page_num + 1, i + 1, df))
    
    return all_tables

def save_tables_to_files(tables, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for page_num, table_num, df in tables:
        # Sanitize the filename
        header_names = "_".join([sanitize_filename(name) for name in df.columns])
        output_csv_path = os.path.join(output_dir, f"page_{page_num}_table_{table_num}_{header_names}.csv")
        output_excel_path = os.path.join(output_dir, f"page_{page_num}_table_{table_num}_{header_names}.xlsx")
        df.to_excel(output_excel_path, index=False)
        # Save to CSV with UTF-8-SIG encoding
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print(f"Table {table_num} on page {page_num} saved to {output_csv_path}")

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\n]', '_', name)

# Example usage
pdf_path = "../examplepdf/color.pdf"  # Replace with your actual PDF path
output_dir = "./output_tables"

tables = extract_tables_from_pdf(pdf_path)
if tables:
    save_tables_to_files(tables, output_dir)
else:
    print("No tables found in the entire document.")