## Note for kaggle

文件夹/pymupdf-venv 建议删掉自己重配一遍

pymupdf参考文档 https://pymupdf.readthedocs.io/en/latest/



```shell
py -m venv pymupdf-venv
.\pymupdf-venv\Scripts\activate
python -m pip install --upgrade pip
pip install --upgrade pymupdf
```

```
pip install JPype1
pip install tabula-py
pip install pandas
pip uninstall camelot
pip uninstall camelot-py
pip install camelot-py[cv]
```



camelot遇见此报错解决方法：

```
DeprecationError(msg) PyPDF2.errors.DeprecationError: PdfFileReader is deprecated and was removed in PyPDF2 3.0.0. Use PdfReader instead.
```

```
你遇到的问题是由于 PyPDF2 库的更新，PdfFileReader 已被弃用并在 PyPDF2 3.0.0 中移除。你需要更新 camelot 代码以使用 PdfReader。

首先，确保你的 PDF 文件路径是正确的。错误信息显示找不到文件 ../example.pdf，请确认文件路径是否正确。

其次，更新 camelot 代码以使用 PdfReader。你可以尝试以下步骤：

更新 camelot 代码：

找到 camelot 库的安装路径。
打开 handlers.py 文件。
将 PdfFileReader 替换为 PdfReader。
手动修改 camelot 源代码：

打开 D:\LTYPolyU\kaggle\Code\pymupdf-venv\Lib\site-packages\camelot\handlers.py 文件。
找到 PdfFileReader 的导入和使用位置，将其替换为 PdfReader。
```

```python
# Code\pymupdf-venv\Lib\site-packages\camelot\handlers.py

# -*- coding: utf-8 -*-

import os
import sys

from PyPDF2 import PdfReader, PdfWriter

from .core import TableList
from .parsers import Stream, Lattice
from .utils import (
    TemporaryDirectory,
    get_page_layout,
    get_text_objects,
    get_rotation,
    is_url,
    download_url,
)


class PDFHandler(object):
    """Handles all operations like temp directory creation, splitting
    file into single page PDFs, parsing each PDF and then removing the
    temp directory.

    Parameters
    ----------
    filepath : str
        Filepath or URL of the PDF file.
    pages : str, optional (default: '1')
        Comma-separated page numbers.
        Example: '1,3,4' or '1,4-end' or 'all'.
    password : str, optional (default: None)
        Password for decryption.

    """

    def __init__(self, filepath, pages="1", password=None):
        if is_url(filepath):
            filepath = download_url(filepath)
        self.filepath = filepath
        if not filepath.lower().endswith(".pdf"):
            raise NotImplementedError("File format not supported")

        if password is None:
            self.password = ""
        else:
            self.password = password
            if sys.version_info[0] < 3:
                self.password = self.password.encode("ascii")
        self.pages = self._get_pages(self.filepath, pages)

    def _get_pages(self, filepath, pages):
        """Converts pages string to list of ints.

        Parameters
        ----------
        filepath : str
            Filepath or URL of the PDF file.
        pages : str, optional (default: '1')
            Comma-separated page numbers.
            Example: '1,3,4' or '1,4-end' or 'all'.

        Returns
        -------
        P : list
            List of int page numbers.

        """
        page_numbers = []
        if pages == "1":
            page_numbers.append({"start": 1, "end": 1})
        else:
            instream = open(filepath, "rb")
            infile = PdfReader(instream, strict=False)
            if infile.is_encrypted:
                infile.decrypt(self.password)
            if pages == "all":
                page_numbers.append({"start": 1, "end": len(infile.pages)})
            else:
                for r in pages.split(","):
                    if "-" in r:
                        a, b = r.split("-")
                        if b == "end":
                            b = len(infile.pages)
                        page_numbers.append({"start": int(a), "end": int(b)})
                    else:
                        page_numbers.append({"start": int(r), "end": int(r)})
            instream.close()
        P = []
        for p in page_numbers:
            P.extend(range(p["start"], p["end"] + 1))
        return sorted(set(P))

    def _save_page(self, filepath, page, temp):
        """Saves specified page from PDF into a temporary directory.

        Parameters
        ----------
        filepath : str
            Filepath or URL of the PDF file.
        page : int
            Page number.
        temp : str
            Tmp directory.

        """
        with open(filepath, "rb") as fileobj:
            infile = PdfReader(fileobj, strict=False)
            if infile.is_encrypted:
                infile.decrypt(self.password)
            fpath = os.path.join(temp, f"page-{page}.pdf")
            froot, fext = os.path.splitext(fpath)
            p = infile.pages[page - 1]
            outfile = PdfWriter()
            outfile.add_page(p)
            with open(fpath, "wb") as f:
                outfile.write(f)
            layout, dim = get_page_layout(fpath)
            # fix rotated PDF
            chars = get_text_objects(layout, ltype="char")
            horizontal_text = get_text_objects(layout, ltype="horizontal_text")
            vertical_text = get_text_objects(layout, ltype="vertical_text")
            rotation = get_rotation(chars, horizontal_text, vertical_text)
            if rotation != "":
                fpath_new = "".join([froot.replace("page", "p"), "_rotated", fext])
                os.rename(fpath, fpath_new)
                instream = open(fpath_new, "rb")
                infile = PdfReader(instream, strict=False)
                if infile.is_encrypted:
                    infile.decrypt(self.password)
                outfile = PdfWriter()
                p = infile.pages[0]
                if rotation == "anticlockwise":
                    p.rotateClockwise(90)
                elif rotation == "clockwise":
                    p.rotateCounterClockwise(90)
                outfile.add_page(p)
                with open(fpath, "wb") as f:
                    outfile.write(f)
                instream.close()

    def parse(
        self, flavor="lattice", suppress_stdout=False, layout_kwargs={}, **kwargs
    ):
        """Extracts tables by calling parser.get_tables on all single
        page PDFs.

        Parameters
        ----------
        flavor : str (default: 'lattice')
            The parsing method to use ('lattice' or 'stream').
            Lattice is used by default.
        suppress_stdout : str (default: False)
            Suppress logs and warnings.
        layout_kwargs : dict, optional (default: {})
            A dict of `pdfminer.layout.LAParams <https://github.com/euske/pdfminer/blob/master/pdfminer/layout.py#L33>`_ kwargs.
        kwargs : dict
            See camelot.read_pdf kwargs.

        Returns
        -------
        tables : camelot.core.TableList
            List of tables found in PDF.

        """
        tables = []
        with TemporaryDirectory() as tempdir:
            for p in self.pages:
                self._save_page(self.filepath, p, tempdir)
            pages = [os.path.join(tempdir, f"page-{p}.pdf") for p in self.pages]
            parser = Lattice(**kwargs) if flavor == "lattice" else Stream(**kwargs)
            for p in pages:
                t = parser.extract_tables(
                    p, suppress_stdout=suppress_stdout, layout_kwargs=layout_kwargs
                )
                tables.extend(t)
        return TableList(sorted(tables))

```

![image-20240921221535217](D:\LTYPolyU\kaggle\ExamplePdf\line.png)


