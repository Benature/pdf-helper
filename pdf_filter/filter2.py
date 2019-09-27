# filter1.py
# version: 1.0
# Date: 2019.09.26
# Author: Benature

import os
import numpy as np
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader


# ========== Config ==================
path = "path/to/lec/pdf"
ignore_files = [
    "pdf_that_u_don't_want_to_filtrate1.pdf",
    "pdf_that_u_don't_want_to_filtrate2.pdf"
]
# ====================================


THRESHOLD_PAGE = 0.1
ANTITHESIS = 255
THRESHOLD_COLOR = ANTITHESIS * 0.01

FLAG = "[s]"


def splitPdf(file_path, pages):
    assert file_path[-4:] == '.pdf'
    root_path, file_name = get_dir_name(file_path)
    output = PdfFileWriter() 
    pdf_raw = PdfFileReader(open(file_path, "rb")) 
    for i in pages: 
        output.addPage(pdf_raw.getPage(i)) 
    outputStream = open(root_path + FLAG + file_name, "wb") 
    output.write(outputStream)


def get_dir_name(file_dir):
    base_name = os.path.basename(file_dir) 
    dir_name = os.path.dirname(file_dir) + "/" 
    return dir_name, base_name


def pdf_filter(file_path):
    pages = convert_from_path(file_path, 10)

    pages = [page.convert("L") for page in pages]

    arrs = [np.array(page) for page in pages]
    SIZE = arrs[0].size
    LEN = len(arrs)

    change_pages = []
    for ind in range(len(arrs) - 1):
        diff_area = arrs[ind] - arrs[ind + 1]
        diff_rate = (diff_area != 0).sum() / SIZE
        diff_x, diff_y = np.where(diff_area != 0)   
        DIFF_strict = False  # 严格判断
        for x, y in zip(diff_x, diff_y):
            if np.abs(arrs[ind][x, y] - ANTITHESIS) > THRESHOLD_COLOR:
                DIFF_strict = True
                break
        if DIFF_strict:
            change_pages.append(ind)
    change_pages.append(LEN - 1)

    print("filtrate out pages", len(change_pages))

    splitPdf(file_path, change_pages)


def main(print_tips = True):
    if path[-4:] != ".pdf":
        # a path of folder
        root_path = path.replace("\\", "/").rstrip("/") + "/"  # 以防万一最后没加斜杠
        filenames = os.listdir(path)
        filenames2 = filenames.copy()
        for fn in filenames:
            if fn.split(".")[-1] != "pdf":
                filenames2.remove(fn)
                continue
            if FLAG in fn:
                filenames2.remove(fn)
                try:
                    filenames2.remove(fn.replace(FLAG, ""))
                except:
                    pass
        for igf in ignore_files:
            if igf in filenames2:
                filenames2.remove(igf)
        for fn in filenames2:
            fn = str(fn)
            print("begin filtrate:", fn)
            if print_tips:
                print("if you don't want to filtrate this file, \nyou can `ctrl+c` to kill the mission \nand add the file name in the `ignore_file` list.\n")
            pdf_filter(root_path + fn)
    else:
        # single one pdf file
        assert path[-4:] == '.pdf', "are you sure it is a pdf file?"
        print("begin filtrate:", path)
        pdf_filter(path)
    print("\n", "="*30)
    print("Finish Filtrating!")
    print("Thank you for your using and waiting")


if __name__ == "__main__":
    main(print_tips=True)
