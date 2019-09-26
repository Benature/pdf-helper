# PDF 过滤器

## 目的

pdf课件为了呈现出动画效果而包含了许多**过程**页面, 本程序针对**有用**页面进行提取.

## 依赖

```python
import os
import numpy as np
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader  
```

>注意: pdf2image的安装需要另外的依赖, 具体参考[文档](https://github.com/Belval/pdf2image)

## 补充

文件写了两个版本, 两者过滤pdf的思路是不一样的.
