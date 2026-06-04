# <center><font face="仿宋" font color=orange>电脑常见操作</font>
### 一、mingw
1. **下载压缩包**
   https://sourceforge.net/projects/mingw-w64/
   文件>>面向win64的工具链>>个人构建>>mingw构建>>(版本8.1.0>>posix>>seh>>下载链接https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-posix/seh/x86_64-8.1.0-release-posix-seh-rt_v6-rev0.7z/download)
   最好使用梯子或迅雷
2. **解压**
   解压到D盘
3. **配置环境变量**
   右键此电脑>>属性>>高级系统设置>>环境变量>>系统变量>>path>>新建>>粘贴解压好的mingw bin 的路径
   检测方式：win+R>>cmd>>输入gcc -v>>有没有出现gcc version 8.1.0
### 二、vs配置
1. **扩展**
   c/c++
   c/c++ compile
2. **配置环境**
   新建一个为c语言的文本文件>>保存>>ctr+shi+P搜索c/c++>>编辑配置(ui)>>编译器路径换gcc>>intellisense模式中选gcc x64>>左上角三点选终端>>编辑任务>>选c/c++：gcc.exe生成活动文件>>回到代码 左上终端>>选择运行生成任务>>选择c/c++：gcc.exe生成活动文件>>回到代码运行即可(用左上角终端可新建终端)
    