# # def show_image(item, title=""):
# #     """Display a pixmap.

# #     Just to display Pixmap image of "item" - ignore the man behind the curtain.

# #     Args:
# #         item: any PyMuPDF object having a "get_pixmap" method.
# #         title: a string to be used as image title

# #     Generates an RGB Pixmap from item using a constant DPI and using matplotlib
# #     to show it inline of the notebook.
# #     """    
# #     DPI = 150  # use this resolution
# #     import numpy as np
# #     import matplotlib.pyplot as plt

# #     # %matplotlib inline
# #     pix = item.get_pixmap(dpi=DPI)
# #     img = np.ndarray([pix.h, pix.w, 3], dtype=np.uint8, buffer=pix.samples_mv)
# #     plt.figure(dpi=DPI)  # set the figure's DPI
# #     plt.title(title)  # set title of image
# #     _ = plt.imshow(img, extent=(0, pix.w * 72 / DPI, pix.h * 72 / DPI, 0))



# import fitz  # import PyMuPDF
# if not hasattr(fitz.Page, "find_tables"):
#     raise RuntimeError("This PyMuPDF version does not support the table feature")

# doc = fitz.open("../examplepdf/chinese-table.pdf")
# page = doc[0]

# tabs = page.find_tables()  # detect the tables
# for i,tab in enumerate(tabs):  # iterate over all tables
#     # for cell in tab.cells:
#     # # Remove extra newlines or spaces

#     #     cell.text = cell.text.replace('\n', ' ').strip()
#     for cell in tab.header.cells:
#         page.draw_rect(cell,color=fitz.pdfcolor["red"],width=0.3)
#     page.draw_rect(tab.bbox,color=fitz.pdfcolor["green"])
#     print(f"Table {i} column names: {tab.header.names}, external: {tab.header.external}")
    
# ## show_image(page, f"Table & Header BBoxes")

# # choose the first table for conversion to a DataFrame
# tab = tabs[0]
# df = tab.to_pandas()

# # show the DataFrame
# # print(df)
# print(tabs[0].extract())

# csv_path = "extracted_table.csv"
# df.to_csv(csv_path, index=False, encoding='utf-8-sig')  ## chinese characters
# print(f"Table saved to {csv_path}")



# perform well for blocked tables like chinese-table.pdf
# but cannot regonize colored tables
# and cannnot regonize the header and lined tables

import fitz  # import PyMuPDF
import pandas as pd

if not hasattr(fitz.Page, "find_tables"):
    raise RuntimeError("This PyMuPDF version does not support the table feature")

file_path = "../examplepdf/chinese-table.pdf"
output_path = "./output_tables/extracted_table"
doc = fitz.open(file_path)

#  just try first page
page = doc[0]

tabs = page.find_tables()  # detect the tables
for tab in tabs:  # iterate over all tables
    #     cell.text = cell.text.replace('\n', ' ').strip()

    # conversion to a DataFrame
    df = tab.to_pandas()
    df.to_csv(output_path+ ".csv", index=False, encoding='utf-8-sig')  ## chinese characters
    df.to_excel(output_path +".xlsx", index=False)
    print(f"Table saved to {output_path}")

