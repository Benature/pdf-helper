import io
from pdf2image import convert_from_path
import img2pdf

file_path = "/Users/benature/OneDrive - LOSA/3_Project/1_QuantumMetrology/Reference/(Mathematics in Science and Engineering 123) Carl W. Helstrom (Eds.) - Quantum Detection and Estimation Theory-Elsevier, Academic Press (1976).pdf"
output_path = 'test.pdf'


def img2bytes(roiImg):
    imgByteArr = io.BytesIO()
    roiImg.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def main():
    pages = convert_from_path(file_path)

    cropped_pages = []
    for page in pages:
        w, h = page.size  # 因为每一页的 size 可能都会不一样
        cropped_pages.append(page.crop([0, 0, w/2, h]))  # 左上 (x,y) - 右下(x,y)
        cropped_pages.append(page.crop([w / 2, 0, w, h]))

    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(
            [img2bytes(cp) for cp in cropped_pages]
        ))


if __name__ == "__main__":
    main()
