from nonebot import require
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters.cqhttp.event import GroupMessageEvent

from .model import load_dict
load_dict()

group_message = GROUP_MEMBER | GROUP_ADMIN | GROUP_OWNER

# 早上好相关模块
good_morning = on_command(
    "good_morning", aliases={"早", "早呀", "早安", "早上好"},
    permission=group_message, rule=to_me(), priority=5)


@good_morning.handle()
async def good_morning_response(bot: Bot, event: Event, state: T_State):
    from .good_morning_function import say_good_morning_to
    msg = say_good_morning_to(event.sender)
    await good_morning.send(msg, at_sender=True)


# 晚安相关模块
good_night = on_command(
    "good_night", aliases={"晚", "晚安"},
    permission=group_message, rule=to_me(), priority=5)


@good_night.handle()
async def good_night_response(bot: Bot, event: Event, state: T_State):
    from .good_morning_function import say_good_night_to
    msg = say_good_night_to(event.sender)
    if msg != '':
        await good_night.send(msg, at_sender=True)


# 守夜人模块
p_night_watch_notice = 30
night_watch = on_command(
    "night_watch", aliases={""},
    permission=group_message, priority=5, block=False)


@night_watch.handle()
async def night_watch_response(bot: Bot, event: Event, state: T_State):
    from .model import night_dict
    if event.sender.user_id.__str__() in night_dict:
        from random import randint
        global p_night_watch_notice
        tmp = randint(1, p_night_watch_notice)
        if tmp == 1:
            p_night_watch_notice = 30
            await good_night.send('你现在不应该在睡觉嘛(ФωФ)', at_sender=True)
        else:
            p_night_watch_notice -= 1


# 让我揉揉模块（你群特色）
let_me_fuck = on_command(
    "let_me_fuck", aliases={"让我揉揉", "让我日日", "让我挼挼", "rwrr", "gwrr", "给我揉揉", "给我挼挼", "给我日日"},
    permission=group_message, rule=to_me(), priority=5)


@let_me_fuck.handle()
async def let_me_fuck_response(bot: Bot, event: Event, state: T_State):
    from .good_morning_function import say_hentai
    msg = say_hentai()
    if msg != '':
        await let_me_fuck.send(msg, at_sender=True)


# 下午三点定时提醒饮茶模块
scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job("cron", hour='15', minute='15', second='00', id="3_oclock_drink_tea")
async def time_3_to_drink_tea():
    from nonebot import get_bots
    from .model import bot_id
    bot_dict = get_bots()
    if not bot_dict.__contains__(bot_id):
        return
    bot = bot_dict[bot_id]
    await bot.send_group_msg(group_id=864515208, message=f'喂！三点几嚟！做 做撚啊做！饮茶先啦！三点几饮 饮茶先啦！做咁多都冇用嘅！老细唔锡你嘅嚟！喂饮下茶先啊！三点几嚟！做碌鸠啊做！')


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job("cron", hour='19', minute='10', second='00', id="7_oclock_drink_beer")
async def time_7_to_drink_beer():
    from nonebot import get_bots
    from .model import bot_id
    bot_dict = get_bots()
    if not bot_dict.__contains__(bot_id):
        return
    bot = bot_dict[bot_id]
    await bot.send_group_msg(group_id=864515208, message=f'喂，朋友，做咩咁多啦？差唔多七点嘞，放工啦，唔使做咁多啦！做咁多，钱带去边度？差唔多七点嘞！放工，焗杯茶沙，饮下靓靓嘅beer，白啤酒黑啤酒OK?happy下 唔使做咁多，死咗都冇用嘞，银纸都冇得带去嘞，happy下，饮酒，OK？')


# 每分钟自动存档
@scheduler.scheduled_job("cron", second='00', id="morning_backup")
async def morning_dict_backup():
    from .model import save_dict
    save_dict()
