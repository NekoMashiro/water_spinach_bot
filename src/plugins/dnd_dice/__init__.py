from nonebot import require
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters.cqhttp.event import GroupMessageEvent

group_message = GROUP_MEMBER | GROUP_ADMIN | GROUP_OWNER

dnd_dice = on_command(
    "dnd_dice", aliases={"/dice"},
    permission=group_message, priority=5)


@dnd_dice.handle()
async def dnd_dice_response(bot: Bot, event: Event, state: T_State):
    content = event.message.__str__().split(' ')[-1]
    dice_list = content.split('+')
    point = 0
    from random import randint
    for dice in dice_list:
        if 'd' in dice:
            time = int(dice.split('d')[0])
            maxn = int(dice.split('d')[1])
            for i in range(time):
                point += randint(1, maxn)
        else:
            point += int(dice)
    await dnd_dice.send(f'摇到的点数是{point}点哦~', at_sender=True)
