# 使用说明
1. 创建python虚拟环境
2. 安装所需要的模块
```
pip install -r requirements/dev.txt
#书上第120页有说明
```
3. 初始化数据库
4. 要为role表添加数据，即创建角色。
```
(venv) $ flask shell
>>> Role.insert_roles()
```

5. 运行项目
```
# Windows PowerShell下的运行方式
$env:FLASK_APP='flasky.py'
$env:FLASK_DEBUG=1
flask run
```
