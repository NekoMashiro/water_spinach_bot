from nonebot import require
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from .pokemon import *
from .battle import *
import time

group_message = GROUP_MEMBER | GROUP_ADMIN | GROUP_OWNER
battle_status = False

pokemon_battle = on_command(
    "pokemon_battle", aliases={"/宝可梦对战"},
    permission=group_message, priority=5)


@pokemon_battle.handle()
async def pokemon_battle_response(bot: Bot, event: Event, state: T_State):
    content = event.message.__str__().split(' ')[-1]
    input_list = content.split('VS')
    if len(input_list) != 2 or input_list[0] == input_list[1]:
        await pokemon_battle.send(f'两只不同的宝可梦才可以对战哦_(•̀ω•́ 」∠)_', at_sender=True)
        return
    global battle_status
    if battle_status == True:
        await pokemon_battle.send(f'一场火热的对战正在进行中哦，请结束以后再来吧！', at_sender=True)
        return
    a_id, b_id = -1, -1
    for pokemon in pokemon_list:
        if pokemon["name"]["chinese"] == input_list[0]:
            a_id = pokemon["id"]
        elif pokemon["name"]["chinese"] == input_list[1]:
            b_id = pokemon["id"]
    if a_id == 0:
        await pokemon_battle.send(f'找不到名叫{input_list[0]}的宝可梦哦~', at_sender=True)
        return
    if b_id == 0:
        await pokemon_battle.send(f'找不到名叫{input_list[1]}的宝可梦哦~', at_sender=True)
        return

    battle_status = True
    p_a, p_b = new_pokemon(a_id), new_pokemon(b_id)
    battle_data, winner = battle(p_a, p_b)
    await pokemon_battle.send(pokemon_to_string(p_a) + '\n' + pokemon_to_string(p_b))
    for data in battle_data:
        time.sleep(5)
        await pokemon_battle.send(data)
    battle_status = False
