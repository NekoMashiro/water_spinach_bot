from nonebot import require
from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters.cqhttp.event import GroupMessageEvent, MessageEvent

message_buffer = ['', '', '']
repeated = False
group_message = GROUP_MEMBER | GROUP_ADMIN | GROUP_OWNER


async def always_true(bot: Bot, event: MessageEvent, state: T_State):
    return True

repeater_model = on_message(always_true, permission=group_message, priority=9)


@repeater_model.handle()
async def repeater_model_handle(bot: Bot, event: Event, state: T_State):
    global repeated, message_buffer
    from random import randint
    message_buffer.insert(0, event.message)
    message_buffer.pop()

    if repeated == False and message_buffer[0] == message_buffer[1] and message_buffer[0] == message_buffer[2]:
        state = randint(0, 3)
        if state == 0:
            repeated = True
            await repeater_model.send(message_buffer[0])
        elif state == 1:
            repeated = True
            await repeater_model.send('复读终结ᐕ)⁾⁾')
    
    if message_buffer[0] != message_buffer[1]:
        repeated = False
