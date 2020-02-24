# PDF 过滤器

详情可阅读[介绍推送](https://mp.weixin.qq.com/s/rVhRRVhk2u1IbalQXwFo2w)

## 简介

pdf课件为了呈现出动画效果而包含了许多**过程**页面, 本程序针对**有用**页面进行提取.

- 对于 latex 生成的 pdf 文件（右下页码），可用[latex_pdf_filter.py](./latex_pdf_filter.py)处理，正确率应当是 100% 的。
- 更 general 的处理可以用[filter1.py](filter1.py)和[filter2.py](filter2.py)处理。

## 补充

- 非 latex 情况文件写了两个版本, 两者过滤pdf的思路是不一样的.
- pdf2image的安装需要另外的依赖, 具体参考[文档](https://github.com/Belval/pdf2image)

> 如果觉得有帮助就给个star呗
