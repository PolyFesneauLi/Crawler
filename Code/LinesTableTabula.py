import tabula
import pandas as pd
import re
import os


### can extract first page of 2.pdf but cannot reconize the second page

def extract_tables_from_pdf(pdf_path):
    # Extract all tables from the PDF using tabula
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    
    if len(tables) == 0:
        print("No tables found!")
        return None
    
    return tables

def save_table_to_files(tables, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize Excel writer
    excel_path = os.path.join(output_dir, "output_tables.xlsx")
    excel_writer = pd.ExcelWriter(excel_path, engine='openpyxl')

    for idx, df in enumerate(tables):
        # Clean up: replace unwanted newlines or other issues
        df = df.applymap(lambda x: x.replace('\n', ' ').strip() if isinstance(x, str) else x)
        
        # Save each table to a separate sheet in the Excel file
        sheet_name = f'Table_{idx + 1}'
        df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
        
        # Save each table to a separate CSV file
        csv_file_path = os.path.join(output_dir, f"table_{idx + 1}.csv")
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        print(f"Table {idx + 1} saved to {csv_file_path}")

    # Save the Excel file
    excel_writer.book.save(excel_path)
    print(f"All tables saved to {excel_path}")

# Function to sanitize file names
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\n]', '_', name) 

# Example usage
pdf_path = "../examplepdf/1.pdf"  
output_dir = "./output_tables"

tables = extract_tables_from_pdf(pdf_path)
if tables:
    save_table_to_files(tables, output_dir)
else:
    print("No tables found in the document.")