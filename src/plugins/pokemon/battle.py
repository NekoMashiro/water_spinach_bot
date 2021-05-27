from .pokemon import *
from random import randint

abilities_map = {}
with open('./datebase/pokemon/abilities.json', encoding='utf-8') as f:
    abilities_list = json.loads(f.read())
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


def calc_dmg(a, b, ability):
    msg = f'{a["name"]["chinese"]}使用了{ability["cname"]}，'

    if ability["power"] == 0:
        return 0, msg + f"然而什么都没有发生……"
    if ability["accuracy"] - 5 < randint(1, 100):
        return 0, msg + f'没有命中！'

    dmg = 0.84
    bonus = 1.0

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
            return 0, msg + f"好像对{b['name']['chinese']}没有效果……"
    if bonus > 1.5:
        msg += "效果绝佳！"
    elif bonus < 0.75:
        msg += "好像效果不好……"
    if ability["type"] in a["type"]:
        bonus *= 1.5
    if randint(1, 12) == 12:
        bonus *= 1.5
        msg += "击中了要害！"
    bonus *= randint(85, 100) / 100

    atk_type = "Attack" if ability["category"] == "physical" else "Sp. Attack"
    def_type = "Defense" if ability["category"] == "physical" else "Sp. Defense"
    atk_value = calc_real_value(
        a["base"][atk_type], a["extra"][atk_type], False)
    def_value = calc_real_value(
        a["base"][def_type], a["extra"][def_type], False)
    dmg = dmg * atk_value / def_value * ability["power"] + 2

    import math
    return math.floor(dmg * bonus), msg


m = {}


def battle(a, b):
    if calc_real_value(a["base"]["Speed"], a["extra"]["Speed"], False) < calc_real_value(b["base"]["Speed"], b["extra"]["Speed"], False):
        a, b = b, a
    a_hp = calc_real_value(a["base"]["HP"], a["extra"]["HP"], True)
    b_hp = calc_real_value(b["base"]["HP"], b["extra"]["HP"], True)
    battle_data = []
    winner = ''

    while True:
        a_atk, a_msg = calc_dmg(a, b, random_ability(a))
        if a_atk > 0:
            a_msg += f'造成了{a_atk}点伤害。'
        b_hp -= a_atk
        if b_hp <= 0:
            a_msg += f'{b["name"]["chinese"]}倒下了，获胜者是{a["name"]["chinese"]}'
            m[a["name"]["chinese"]] += 1
            winner = a["name"]["chinese"]
            battle_data.append(a_msg)
            break
        a_msg += f'{a["name"]["chinese"]}还剩{a_hp}HP，{b["name"]["chinese"]}还剩{b_hp}HP'
        battle_data.append(a_msg)

        b_atk, b_msg = calc_dmg(b, a, random_ability(b))
        if b_atk > 0:
            b_msg += f'造成了{b_atk}点伤害。'
        a_hp -= b_atk
        if a_hp <= 0:
            b_msg += f'{a["name"]["chinese"]}倒下了，获胜者是{b["name"]["chinese"]}'
            m[b["name"]["chinese"]] += 1
            winner = a["name"]["chinese"]
            battle_data.append(b_msg)
            break
        b_msg += f'{a["name"]["chinese"]}还剩{a_hp}HP，{b["name"]["chinese"]}还剩{b_hp}HP'
        battle_data.append(b_msg)

    return battle_data, winner


p1 = new_pokemon(291)
p2 = new_pokemon(438)
m[p1["name"]["chinese"]] = 0
m[p2["name"]["chinese"]] = 0
print(pokemon_to_string(p1))
print(pokemon_to_string(p2))
battle_data, winner = battle(p1, p2)
for i in battle_data:
    print(i)
