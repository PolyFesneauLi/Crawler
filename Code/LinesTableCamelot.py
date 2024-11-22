

### 5.pdf 会丢失第一行
### 1.pdf 不理想，后面的数据对齐有误
### chinese 分行糟糕
### color 分列有问题，间隔设置小的话会错列

# 可以不导入 pandas，因为导入该库时会自动导入 pandas
import camelot.io as camelot
 
# 解析表格
result = camelot.read_pdf(
            # filepath="../examplepdf/1.pdf",  # 94
            filepath="../examplepdf/1.pdf",  # 94
            pages='all', 
            # 针对不同类型的PDF表格指定解析方式，可选参数有'lattice'（格子解析）和'stream'（流解析），前者适用于解析带有完整框线的表格，后者常用于解析框线不全的表格。
            flavor='stream',  # 'stream' or 'lattice' depending on your needs
            ## 如果表格的某两行之间间隙稍大，导致表格解析被解析为多个表格，那么可以增加该参数的值，避免读取的表格不完整
            edge_tol=1000,   
            ## 当单元格中有分行的文本时，是否应该将它们分为多个单元格
            split_text = True,
            ## 去除单元格中的指定字符，默认值为''，即不清洗，如果需要取出多种不需要的字符，那么直接将多个字符组合成一个字符串传入即可
            strip_text='\n'         
                         )
                         
# 解析结果中可能包含多个表格，下面把解析到的第一个表格转为 DataFrame
# 如果解析结果中不含表格，那么将会报错

# just try first table
df = result[0].df
df.to_csv("output.csv", index=False, encoding='utf-8-sig')
df.to_excel("output.xlsx", index=False)

# 效果不好，解析的支离破碎的

# import fitz  # PyMuPDF

# # Open the PDF file
# pdf_document = '../examplepdf/chinese-table.pdf'
# doc = fitz.open(pdf_document)

# # Extract text and filter for table-like structures
# text = ""
# for page in doc:
#     text += page.get_text()

# # Split text into lines
# lines = text.split('\n')

# # Define a function to determine if a line is part of a table
# def is_table_line(line):
#     # Example: Check if the line contains numeric data or follows a pattern
#     return any(char.isdigit() for char in line)

# # Collect only table-like lines
# table_lines = [line for line in lines if is_table_line(line)]

# # Process the lines into a structured format
# data = []
# for line in table_lines:
#     parts = line.split()
#     data.append(parts)

# # Save the structured data to CSV
# with open('output.csv', 'w', encoding='utf-8-sig') as f:
#     for row in data:
#         f.write(','.join(row) + '\n')

# print('Table data saved to output.csv')