import math
from .pokemon import *
from random import randint

abilities_map = {}
with open('./datebase/pokemon/abilities.json', encoding='utf-8') as f:
    content = f.read()
    abilities_list = json.loads(content)
    for ability in abilities_list:
        tp = ability["type"]
        if tp not in abilities_map:
            abilities_map[tp] = []
        abilities_map[tp].append(ability)
    f.close()


def random_ability(pokemon):
    tp_num = randint(0, 23)
    if tp_num < 12:
        tp_str = basic_type_with_effect[tp_num]['english']
    else:
        tp_num = randint(0, len(pokemon["type"]) - 1)
        tp_str = pokemon["type"][tp_num]
    ab = abilities_map[tp_str][randint(0, len(abilities_map[tp_str]) - 1)]
    return ab


def calc_dmg(a, b, evade, ability):
    msg = f'{a["name"]["chinese"]}挥指，使出了{ability["cname"]}，'

    if ability["accuracy"] - evade < randint(1, 100):
        return 0, 0, 0, "", msg + f'没有命中！'

    bonus = 1.0
    dmg = 0
    if ability['power'] != 0:
        for i in range(18):
            if basic_type_with_effect[i]["english"] == ability["type"]:
                ab_index = i
                break
        for btype in b["type"]:
            if btype in basic_type_with_effect[ab_index]["effect_double"]:
                bonus *= 2.0
            elif btype in basic_type_with_effect[ab_index]["effect_half"]:
                bonus *= 0.5
            elif btype in basic_type_with_effect[ab_index]["effect_zero"]:
                return 0, 0, 0, "", msg + f"好像对{b['name']['chinese']}没有效果……"
        if bonus > 1.5:
            msg += "效果绝佳！"
        elif bonus < 0.75:
            msg += "好像效果不好……"
        if ability["type"] in a["type"]:
            bonus *= 1.5

        ct_value = 1
        if "critical" in ability["extra"]:
            ct_value = ability["extra"]["critical"]
        if randint(1, 12) <= ct_value:
            bonus *= 1.5
            msg += "击中了要害！"
        bonus *= randint(85, 100) / 100

        atk_type = "Attack" if ability["category"] == "physical" else "Sp. Attack"
        def_type = "Defense" if ability["category"] == "physical" else "Sp. Defense"
        atk_value = calc_real_value(
            a["base"][atk_type], a["extra"][atk_type], False)
        def_value = calc_real_value(
            a["base"][def_type], a["extra"][def_type], False)
        dmg = 0.84 * atk_value / def_value * ability["power"] + 2
    heal = 0
    a_add_evade = 0
    b_status = ""
    if "heal" in ability["extra"]:
        max_hp = calc_real_value(a["base"]["HP"], a["extra"]["HP"], True)
        heal = math.floor(max_hp * ability["extra"]["heal"] / 100)
        msg += f"回复了{heal}点HP！"
    if "life_steal" in ability["extra"]:
        heal = math.floor(dmg * bonus * ability["extra"]["life_steal"] / 100)
        msg += f"吸取了{heal}点HP！"
    if "add_evade" in ability["extra"]:
        if randint(1, 100) <= ability["extra"]["add_evade"]:
            a_add_evade = 5
            msg += f"{b['name']['chinese']}的命中率降低了！"
    if "paralysis" in ability["extra"]:
        if randint(1, 100) <= ability["extra"]["paralysis"]:
            b_status = "paralysis"
            msg += f"{b['name']['chinese']}麻痹了，可能无法动弹（本版本不附带减速效果）"
    if "flinch" in ability["extra"]:
        if randint(1, 100) <= ability["extra"]["flinch"]:
            b_status = "flinch"
            msg += f"{b['name']['chinese']}畏缩了，下次行动无法使出招式！"
    if "poison" in ability["extra"]:
        if randint(1, 100) <= ability["extra"]["poison"]:
            b_status = "poison"
            msg += f"{b['name']['chinese']}中毒了！每回合将损失1/8HP！"
    if "burn" in ability["extra"]:
        if randint(1, 100) <= ability["extra"]["burn"]:
            b_status = "burn"
            msg += f"{b['name']['chinese']}灼伤了！每回合将损失1/8HP！（本版本简化成和中毒一样的效果）"
    if "freeze" in ability["extra"]:
        if randint(1, 100) <= ability["extra"]["freeze"]:
            b_status = "freeze"
            msg += f"{b['name']['chinese']}冰冻了！每回合将损失1/8HP！（本版本简化成和中毒一样的效果）"

    return math.floor(dmg * bonus), heal, a_add_evade, b_status, msg


m = {}


def win(a, b):
    msg = f'{b["name"]["chinese"]}倒下了，获胜者是{a["name"]["chinese"]}'
    if a["name"]["chinese"] not in m:
        m[a["name"]["chinese"]] = 0
    m[a["name"]["chinese"]] += 1
    winner = a["name"]["chinese"]
    return msg, winner


def battle(a, b):
    if calc_real_value(a["base"]["Speed"], a["extra"]["Speed"], False) < calc_real_value(b["base"]["Speed"], b["extra"]["Speed"], False):
        a, b = b, a
    a_max_hp = calc_real_value(a["base"]["HP"], a["extra"]["HP"], True)
    b_max_hp = calc_real_value(b["base"]["HP"], b["extra"]["HP"], True)
    a_hp, b_hp = a_max_hp, b_max_hp
    a_status = ""
    b_status = ""
    a_evade = 5
    b_evade = 5
    a_paralysis = False
    b_paralysis = False

    battle_data = []
    winner = ''

    while True:
        if a_paralysis == True:
            a_paralysis = False
            a_msg = f'{a["name"]["chinese"]}畏缩了，无法使出招式！'
        elif a_status == 'paralysis' and randint(1, 3) == 1:
            a_msg = f'{a["name"]["chinese"]}麻痹了，无法动弹！'
        else:
            a_atk, a_heal, a_add_evade, b_s, a_msg = calc_dmg(
                a, b, b_evade, random_ability(a))
            if a_atk > 0:
                a_msg += f'造成了{a_atk}点伤害。'
            b_hp -= a_atk
            a_hp += a_heal
            a_hp = min(a_hp, a_max_hp)
            a_evade += a_add_evade
            if b_s != '':
                if b_s == 'flinch':
                    b_paralysis = True
                else:
                    b_status = b_s
            if b_hp <= 0:
                win_msg, winner = win(a, b)
                battle_data.append(a_msg + win_msg)
                break
            a_msg += f'{a["name"]["chinese"]}还剩{a_hp}HP，{b["name"]["chinese"]}还剩{b_hp}HP'
        battle_data.append(a_msg)

        if b_paralysis == True:
            b_paralysis = False
            b_msg = f'{b["name"]["chinese"]}畏缩了，无法使出招式！'
        elif b_status == 'paralysis' and randint(1, 3) == 1:
            b_msg = f'{b["name"]["chinese"]}麻痹了，无法动弹！'
        else:
            b_atk, b_heal, b_add_evade, a_s, b_msg = calc_dmg(
                b, a, a_evade, random_ability(b))
            if b_atk > 0:
                b_msg += f'造成了{b_atk}点伤害。'
            a_hp -= b_atk
            b_hp += b_heal
            b_hp = min(b_hp, b_max_hp)
            b_evade += b_add_evade
            if a_s != '':
                if a_s == 'flinch':
                    a_paralysis = True
                else:
                    a_status = a_s
            if a_hp <= 0:
                win_msg, winner = win(b, a)
                battle_data.append(b_msg + win_msg)
                break
            b_msg += f'{a["name"]["chinese"]}还剩{a_hp}HP，{b["name"]["chinese"]}还剩{b_hp}HP'
        battle_data.append(b_msg)

        o_msg = ""
        if a_status in ["poison", "burn", "freeze"]:
            a_hp -= math.floor(a_max_hp / 8)
            o_msg += f'{a["name"]["chinese"]}正处于{a_status}状态，失去了{math.floor(a_max_hp / 8)}点HP！'
            if a_hp <= 0:
                win_msg, winner = win(b, a)
                battle_data.append(o_msg + win_msg)
                break

        if b_status in ["poison", "burn", "freeze"]:
            b_hp -= math.floor(b_max_hp / 8)
            o_msg += f'{b["name"]["chinese"]}正处于{b_status}状态，失去了{math.floor(b_max_hp / 8)}点HP！'
            if b_hp <= 0:
                win_msg, winner = win(a, b)
                battle_data.append(o_msg + win_msg)
                break

        if o_msg != "":
            battle_data.append(
                o_msg + f'（当前版本毒火冰状态伤害均不计算属性）{a["name"]["chinese"]}还剩{a_hp}HP，{b["name"]["chinese"]}还剩{b_hp}HP')
        print(a_msg + '\n' + b_msg + '\n' + o_msg + '\n--------------------------')
    
    print('--------BATTLE END--------')

    return battle_data, winner


# p1 = new_pokemon(24)
# p2 = new_pokemon(311)
# m[p1["name"]["chinese"]] = 0
# m[p2["name"]["chinese"]] = 0
# print(pokemon_to_string(p1))
# print(pokemon_to_string(p2))
# battle_data, winner = battle(p1, p2)
# for i in battle_data:
#     print(i)
