import copy
from functools import wraps

from nonebot.message import _check_at_me, _check_calling_me_nickname

from hoshino.typing import CQEvent
from hoshino import trigger

evCache = CQEvent({})
conflictCache = True


async def not_conflict(bot, event: CQEvent):
    global evCache, conflictCache
    if event == evCache:
        return conflictCache
    evCache = CQEvent(copy.deepcopy(dict(event)))
    if event.detail_type != 'group':
        conflictCache = False
        return False
    raw_to_me = event.get('to_me', False)
    _check_at_me(bot, event)
    _check_calling_me_nickname(bot, event)
    event['to_me'] = raw_to_me or event['to_me']
    service_funcs = []
    for t in trigger.chain:
        service_funcs.extend(t.find_handler(event))

    if not service_funcs:
        conflictCache = True
        return True

    for service_func in service_funcs:
        if service_func.only_to_me and not event['to_me']:
            continue

        if not service_func.sv._check_all(event):
            continue
        conflictCache = False
        return False
    conflictCache = True
    return True


def anti_conflict(f):
    """
    用途：防止闲聊类插件（或任意全局匹配插件）在其他插件调用指令时触发

    使用方法：在@sv.on_message('group')下
    添加@anti_conflict
    """

    @wraps(f)
    async def decorated(*args, **kwargs):
        ev = CQEvent(copy.deepcopy(dict(args[1])))
        if not await not_conflict(args[0], ev):
            return
        return await f(*args, **kwargs)

    return decorated
