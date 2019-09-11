若您读到此文件，说明这是ODR备份策略开发版本，操作步骤不会详尽说明且仅供手动备份（不设置定时任务）
1，将函数、存储过程 执行至需要备份的数据库中
2，安装python环境及pymssql包（如已经有请忽略此步骤）
3，文本编辑器中打开文件“DbObjectBackup.py”，并仔细阅读文件开头的说明，初始化必要变量，保存
4，返回“readme.txt”所在文件夹，shift+鼠标右键打开cmd，输入：python .\DbObjectBackup.py
5，等待完成