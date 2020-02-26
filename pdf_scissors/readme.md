# PDF Scissors - PDF 剪刀 ✂️

对 pdf 页面进行切割，代码以**双列** pdf 切割为例。

如需切割四宫格或多宫格 pdf，可参考修改下面代码👇

```python
cropped_pages.append(page.crop([0, 0, w/2, h]))  # 左上 (x,y) - 右下(x,y)
cropped_pages.append(page.crop([w / 2, 0, w, h]))
```

</br>
<p align="center">效果图 ✂️</p>
<p align="center">
  <img src="demo.png" width="70%"/>
</p>

>注意：处理后的 pdf 将丢失对文本的选中能力，因为处理方式是转图片后切割再拼接的。如希望选中文本，可以使用 Acrobat👇

<p align="center">
  <img src="acrobat.png" width="60%"/>
</p>
