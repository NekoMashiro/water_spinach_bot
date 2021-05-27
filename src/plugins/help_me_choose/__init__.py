from nonebot import require
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters.cqhttp.event import GroupMessageEvent

group_message = GROUP_MEMBER | GROUP_ADMIN | GROUP_OWNER
help_me_choose = on_command(
    "help_me_choose", aliases={"帮我选", "帮我决定"},
    permission=group_message, rule=to_me(), priority=5)


@help_me_choose.handle()
async def help_me_choose_response(bot: Bot, event: Event, state: T_State):
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·"""
    dicts = {i: ' ' for i in punctuation}
    punc_table = str.maketrans(dicts)
    new_s = event.message.__str__().translate(punc_table)
    list_array = new_s.split(' ')[1:]
    from random import randint
    result = randint(1, len(list_array)) - 1
    await help_me_choose.send(f'真拿你没办法…… 菜菜可能觉得…… { list_array[result] }更好一些吧！', at_sender=True)
