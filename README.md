# hoshino_tool

## @anti_conflict 装饰器

曾用名：闲聊反并发工具

### 用途

用途：防止 AI 聊天类插件（或任意全局匹配插件）在其他插件注册的指令被调用时触发

### 使用方法

1. 将 `tool.py` 添加至 `hoshino` 目录（即 `modules` 的上一级目录）下

2. 在使用了 `@sv.on_message('group')` 的相应 python 文件开头添加 `from hoshino.tool import anti_conflict`

3. 在 `@sv.on_message('group')` 下添加 `@anti_conflict`

### 示例

```python
from hoshino import Service
from hoshino.tool import anti_conflict

sv = Service('example')

# 在 @sv.on_message('group') 下添加 @anti_conflict
# 如果消息符合其他插件注册的触发器，则不会进入 example_handler 函数
@sv.on_message('group')
@anti_conflict
async def example_handler(bot, ev: CQEvent):
    msg = str(ev['message']).strip()
    if msg.startswith(f'[CQ:at,qq={ev["self_id"]}]') or msg.endswith(f'[CQ:at,qq={ev["self_id"]}]'):
        # 示例：处理 @bot 的回复
        # 例如，有插件注册了 @sv.on_keyword('test', only_to_me=True) 的触发器
        # 则一个用户在群聊中发送 '@bot test' 时，不会进入 example_handler 函数，也自然不会触发此处的处理逻辑
        pass
    else:
        # 示例：处理一般规则（例如随机触发的 AI 回复）
        # 例如，有插件注册了 @sv.on_keyword('test') 的触发器
        # 则一个用户在群聊中发送 'test' 时，不会进入 example_handler 函数，也自然不会触发此处的处理逻辑
        # 再者，如果有插件注册了 @sv.on_keyword('test2', only_to_me=True) 的触发器
        # 则一个用户在群聊中发送 'test2' 时，可以正常进入 example_handler 函数，并触发此处的处理逻辑
        pass
```
