import json
file_name = 'E:\\github\\NoneBot\\qbot\\src\\plugins\\pokemon\\table.txt'
with open(file_name, encoding='utf-8') as f:
    file_content = f.read()
    f.close()
table = file_content.split('\n')
file_name = 'E:\\github\\NoneBot\\qbot\\datebase\\pokemon\\types.json'
with open(file_name, encoding='utf-8') as f:
    file_content = f.read()
    f.close()
types_json = json.loads(file_content)
for i in range(18):
    effect_list = table[i].split('\t')
    types_json[i]['effect_double'] = []
    types_json[i]['effect_half'] = []
    types_json[i]['effect_zero'] = []
    for j in range(18):
        if effect_list[j] == '2×':
            types_json[i]['effect_double'].append(types_json[j]['english'])
        if effect_list[j] == '1⁄2×':
            types_json[i]['effect_half'].append(types_json[j]['english'])
        if effect_list[j] == '0×':
            types_json[i]['effect_zero'].append(types_json[j]['english'])

file_name = 'E:\\github\\NoneBot\\qbot\\datebase\\pokemon\\types_with_effect.json'
with open(file_name, 'w', encoding='utf-8') as f:
    s = json.dumps(types_json, ensure_ascii=False)
    f.write(s)
f.close()
