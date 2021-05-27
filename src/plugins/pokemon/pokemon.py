from random import randint
import json
basic_value_map = {"HP": 0, "Attack": 0, "Defense": 0,
                   "Sp. Attack": 0, "Sp. Defense": 0, "Speed": 0}
basic_value_list = ["HP", "Attack", "Defense",
                    "Sp. Attack", "Sp. Defense", "Speed"]
basic_value_etoc = {"HP": "HP", "Attack": "攻击", "Defense": "防御",
                    "Sp. Attack": "特攻", "Sp. Defense": "特防", "Speed": "速度"}
basic_type_with_effect = []
with open('./datebase/pokemon/types_with_effect.json', encoding='utf-8') as f:
    basic_type_with_effect = json.loads(f.read())
    f.close()


def calc_real_value(basic, extra, is_hp):
    if(is_hp == True):
        return basic * 2 + extra + 110
    else:
        return basic * 2 + extra + 5


def add_extra_value(pokemon, ability):
    if ability not in basic_value_list:
        return False
    if pokemon['extra'][ability] > 31:
        return False
    pokemon['extra'][ability] += 1


def random_extra_value():
    extra_value = basic_value_map.copy()
    status = basic_value_list[randint(0, 5)]
    extra_value[status] += 1
    status = basic_value_list[randint(0, 5)]
    extra_value[status] += 4
    status = basic_value_list[randint(0, 5)]
    extra_value[status] += 10
    return extra_value


def new_pokemon(id):
    file_name = './datebase/pokemon/pokedex.json'
    with open(file_name, encoding='utf-8') as f:
        file_content = f.read()
        f.close()
    import json
    pokemon_list = json.loads(file_content)
    pokemon = pokemon_list[id - 1]
    pokemon['extra'] = random_extra_value()
    return pokemon


def random_grow(pokemon):
    for i in range(2):
        status = basic_value_list[randint(0, 5)]
        add_extra_value(pokemon, status)
    return pokemon

def find_type(type_name):
    for tp in basic_type_with_effect:
        if type_name == tp['english']:
            return tp


def pokemon_to_string(pokemon):
    name = f'名称: {pokemon["name"]["chinese"]}\n'

    types = '属性:'
    for t in pokemon["type"]:
        tp = find_type(t)
        types += f' {tp["chinese"]}'
    types += '\n'

    extra = '附加值:'
    for i in pokemon["extra"]:
        if pokemon["extra"][i] != 0:
            extra += f' {basic_value_etoc[i]}+{pokemon["extra"][i]}'

    return name + types + extra
