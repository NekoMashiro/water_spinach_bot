from nonebot import require
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters.cqhttp.event import GroupMessageEvent
import time

game_state = 0
game_start_time = 0
game_group_code = 0
# group_message = GROUP_MEMBER | GROUP_ADMIN | GROUP_OWNER
group_message = GROUP_ADMIN | GROUP_OWNER | GROUP_MEMBER
player_state = {}

# 是规则书哦
blackjack_rule = on_command("/21点", permission=group_message, priority=5)


@blackjack_rule.handle()
async def blackjack_rule_response(bot: Bot, event: Event, state: T_State):
    msg = '开始游戏：昵称+21点\n'
    msg += '加入现有游戏：昵称+我也要玩21点\n'
    msg += '要牌：/要牌    停牌：/停牌\n'
    msg += '庄家规则：低于17点必须要牌\n'
    msg += '注：不提供"5张牌>一切"和"3张7>一切"的规则，最大就是BlackJack！'
    await blackjack_start.send(msg, at_sender=True)


# 游戏开始
blackjack_start = on_command(
    "blackjack_start", aliases={"二十一点", "21点", "来把二十一点", "来把21点", "赌怪", "土块", },
    permission=group_message, rule=to_me(), priority=5)


@blackjack_start.handle()
async def blackjack_start_response(bot: Bot, event: Event, state: T_State):
    global game_state, game_start_time, game_group_code, player_state

    if game_state == 1:
        if time.time() - game_start_time < 300:
            await blackjack_start.send('请等这桌结束吧~菜菜也不会分身呢qwq')
            return
        else:
            await blackjack_start.send('虽然游戏还在进行~不过上一局已经有人五分钟还没结束了诶~那么我们开新局好了qwq！')

    game_state = 1
    game_start_time = time.time()
    game_group_code = event.group_id
    player_state = {}

    from .card_lib import card_game_start, add_player
    player_id = event.sender.user_id
    msg = '那菜菜就当庄家了哦~ ' + card_game_start()
    await blackjack_start.send(msg)

    time.sleep(3)

    player_state[player_id] = 0
    msg = add_player(player_id)
    await blackjack_start.send(msg, at_sender=True)


# 鉴定用户状态
def state_judge(player_id):
    if game_state == 0:
        return '牌桌还没搭呢！'
    if player_id not in player_state:
        return '你还没加入游戏呢！'
    if player_state[player_id] == 1:
        return '你好像已经停牌/爆牌了哦~'
    return ''


def add_player_judge(player_id):
    if game_state == 0:
        return '牌桌还没搭呢！'
    if player_id in player_state:
        return '你已经在玩了吧！'
    if len(player_state) == 8:
        return '一桌最多8个人哦~ 菜菜受不了更多人一起上啦qwq'
    return ''


# 加入游戏
blackjack_add_player = on_command(
    "blackjack_add_player", aliases={"我也要玩21点", "我也要玩二十一点", "我也要当赌怪", "我也要当土块"},
    permission=group_message, rule=to_me(), priority=5)


@blackjack_add_player.handle()
async def blackjack_add_player_response(bot: Bot, event: Event, state: T_State):
    player_id = event.sender.user_id
    msg = add_player_judge(player_id)
    if msg != '':
        await blackjack_ask_card.send(msg, at_sender=True)
        return

    from .card_lib import add_player
    global game_start_time
    game_start_time = time.time()
    player_state[player_id] = 0
    msg = add_player(player_id)
    await blackjack_start.send(msg, at_sender=True)

    # 要牌
blackjack_ask_card = on_command(
    "blackjack_ask_card", aliases={"/要牌"},
    permission=group_message, priority=5)


@blackjack_ask_card.handle()
async def blackjack_ask_card_response(bot: Bot, event: Event, state: T_State):
    player_id = event.sender.user_id
    msg = state_judge(player_id)
    if msg != '':
        await blackjack_ask_card.send(msg, at_sender=True)
        return

    from .card_lib import ask_card, every_player_point, stop_card
    msg = ask_card(player_id)
    await blackjack_ask_card.send(msg, at_sender=True)

    if every_player_point[player_id] == -1:
        player_state[player_id] = 1
        if stop_card(player_id):
            await final_calc(bot)


# 停牌
blackjack_stop_card = on_command(
    "blackjack_stop_card", aliases={"/停牌"},
    permission=group_message, priority=5)


@blackjack_stop_card.handle()
async def blackjack_stop_card_response(bot: Bot, event: Event, state: T_State):
    player_id = event.sender.user_id
    msg = state_judge(player_id)
    if msg != '':
        await blackjack_ask_card.send(msg, at_sender=True)
        return

    from .card_lib import stop_card, every_player_point
    from random import randint

    msg = '那就停牌了哦'
    if randint(1, 10) + every_player_point[player_id] <= 21:
        msg += ' 这不再贪一手_(•̀ω•́ 」∠)_'
    else:
        msg += ' 见好就收什么的最棒了呢'
        if randint(1, 20) == 1:
            msg += ' 日菜菜也是这样的欸嘿嘿嘿'
        msg += '੭ ᐕ)੭*⁾⁾'

    state = stop_card(player_id)
    player_state[player_id] = 1

    await blackjack_ask_card.send(msg, at_sender=True)
    if state == True:
        await final_calc(bot)


async def final_calc(bot: Bot):
    time.sleep(3)
    msg = '看来轮到菜菜了哦\n'
    from .card_lib import every_player_card, every_player_point, card_to_string, calc_handcards_point
    msg += f'菜菜的第二张牌是：{ card_to_string(every_player_card["banker"][1]) }！'
    calc_handcards_point('banker')
    if every_player_point["banker"] == 22:
        msg += f'是Blackjack哦(ФωФ)'
    else:
        msg += f'现在总点数是{ every_player_point["banker"] }点哦'
    await bot.send_group_msg(group_id=game_group_code, message=msg)
    time.sleep(2)

    msg = ''
    pos = 2
    while every_player_point['banker'] < 17 and every_player_point['banker'] != -1:
        from .card_lib import total_card
        every_player_card['banker'].append(total_card.pop())
        calc_handcards_point('banker')
        msg += f'不足17点必须要牌 小空要到的牌是{ card_to_string(every_player_card["banker"][pos]) } '
        if every_player_point['banker'] == -1:
            msg += '爆……爆掉了QAQ'
        else:
            msg += f'总点数是{ every_player_point["banker"] }'

        msg += '\n'
        pos += 1
    if(pos != 2):
        await bot.send_group_msg(group_id=game_group_code, message=msg)
    time.sleep(2)

    winner_num = 0
    winner = []
    for user in player_state:
        if every_player_point[user] > every_player_point['banker']:
            winner.append(
                {"type": "at",
                 "data": {"qq": user.__str__()},
                 },
            )
            winner_num += 1

    if winner_num == 0:
        msg = '你们都不是本菜的对手！'
    elif winner_num == len(player_state) and winner_num > 1:
        msg = '所……所有人都赢了……？你……你们别过来QAQ……'
    else:
        msg = [{"type": "text", "data": {"text": "赢家是"}}] + \
            winner + [{"type": "text", "data": {"text": "哦~"}}]

    await bot.send_group_msg(group_id=game_group_code, message=msg)
    global game_state
    game_state = 0
