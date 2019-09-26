# filter1.py
# version: 1.0
# Date: 2019.09.26
# Author: Benature

import os
import numpy as np
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader  

# ========== Config ==================
file_path = "path/to/lec/pdf"
# ====================================

FRESHOLD = 0.1


def diff_rate(arrs, ind):
    return ((arrs[ind] - arrs[ind + 1]) != 0).sum() / SIZE


def splitPdf(file_path, pages):
    assert file_path[-4:] == '.pdf'
    root_path, file_name = get_dir_name(file_path)
    output = PdfFileWriter() 
    pdf_raw = PdfFileReader(open(file_path, "rb")) 
    for i in pages: 
        output.addPage(pdf_raw.getPage(i)) 
    outputStream = open(root_path + "[s]" + file_name, "wb") 
    output.write(outputStream)


def get_dir_name(file_dir):
    base_name = os.path.basename(file_dir)  # 获得地址的文件名
    dir_name = os.path.dirname(file_dir) + "/"  # 获得地址的父链接
    return dir_name, base_name


pages = convert_from_path(file_path, 10)
pages = [page.convert("L") for page in pages]

arrs = [np.array(page) for page in pages]
SIZE = arrs[0].size
LEN = len(arrs)

change_pages = []
for i in range(len(arrs) - 1):
    if (diff_rate(arrs, i) > FRESHOLD):
        change_pages.append(i)
change_pages.append(LEN - 1)

print("filt out pages", len(change_pages))

splitPdf(file_path, change_pages)