# hoshino_tool

## 用途
防止闲聊类插件（或任意全局匹配插件）在其他插件调用指令时触发

## 使用方法
将tool.py添加至hoshino文件夹
在相应python文件开头添加from hoshino.tool import anti_conflict
在@sv.on_message('group')下添加@anti_conflict
