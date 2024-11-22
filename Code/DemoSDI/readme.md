```
在https://wkhtmltopdf.org/downloads.html 
```

下载对应电脑版本的`wkhtmltopdf`

若win 64 位 直接用我给的安装包安装就行



修改17行路径为本地安装路径

![image-20240926145354482](D:\LTYPolyU\kaggle\Code\DemoSDI\picture\image-20240926145354482.png)

在运行环境下

```
pip install pandas
pip install pdfkit  
...
```

等等，按照报错提示一个个pip install就行了



输出解释：

01398为例 有两行 A股 H股

![image-20240925172230803](D:\LTYPolyU\kaggle\Code\DemoSDI\picture\image-20240925172230803.png)

分别存在两子文件夹

![image-20240925172333916](D:\LTYPolyU\kaggle\Code\DemoSDI\picture\image-20240925172333916.png)

outline是首页，combined是首页＋其他6张表（共7页）的总册



![image-20240925172410284](D:\LTYPolyU\kaggle\Code\DemoSDI\picture\image-20240925172410284.png)

编号的子网页pdf存在相应文件夹下

![image-20240925172538902](D:\LTYPolyU\kaggle\Code\DemoSDI\picture\image-20240925172538902.png)
