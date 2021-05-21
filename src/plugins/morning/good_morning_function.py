def say_good_morning_to(sender):
    uid = sender.user_id.__str__()
    from datetime import datetime
    if datetime.now().hour < 6:
        return '为保证充足睡眠，6点以后才可以起床哦 _(:3 ⌒ﾞ)_'

    from .model import morning_dict
    if uid in morning_dict:
        return '你不是已经起过床了吗 (。・`ω´・)'

    # 性别判断会手动调用API
    sex = '大佬'
    try:
        import json
        import urllib.request
        url = 'http://127.0.0.1:5700/get_stranger_info?user_id=' + uid
        response = urllib.request.urlopen(url)
        info_map = response.read().decode('utf-8')
        info_map = json.loads(info_map)
        sex = '少年' if info_map["data"]["sex"] == "male" else '少女'
    except BaseException:
        pass

    now_time = datetime.time(datetime.now()).__str__()
    morning_dict[uid] = now_time

    from random import randint
    result = randint(1, 10)
    if result == 1:
        return '早什么早 早上要说我爱你！'

    get_up_rank = len(morning_dict).__str__()
    if datetime.now().hour < 9:
        return '你起的很早呢~你是今天第' + get_up_rank + '位起床的' + sex + '哦 (⸝⸝•‧̫•⸝⸝)'
    if datetime.now().hour < 11:
        return '上午好呀~你是今天第' + get_up_rank + '位起床的' + sex + '呢 ┴┤･ω･)ﾉ'
    if datetime.now().hour < 14:
        return '已经是中午了哦~你是今天第' + get_up_rank + '只起床的小懒猫 (›´ω`‹ )'
    if datetime.now().hour < 18:
        return '你是今天第' + get_up_rank + '位起床的小懒鬼~懒死你了(*¯ㅿ¯*;)'
    return '这么晚还不如不起了呢！菜菜不要数你是第几个起床的了！哼(ﾉ｀⊿´)ﾉ'


def say_good_night_to(sender):
    uid = sender.user_id.__str__()
    from .model import morning_dict, night_dict
    if uid not in morning_dict:
        return '不起床就睡，懒死你哦(ﾉ｀⊿´)ﾉ'

    if uid in night_dict:
        return ''

    from datetime import datetime
    if datetime.now().hour > 4 and datetime.now().hour < 19:
        return '为保证规律作息，晚上7点以后才可以睡觉哦 _(:3 ⌒ﾞ)_'

    now_time = datetime.time(datetime.now()).__str__()
    night_dict[uid] = now_time
    if datetime.now().hour > 4 and datetime.now().hour < 20:
        return '晚安哦~你睡得很早呢~ (⸝⸝•‧̫•⸝⸝)'
    if datetime.now().hour > 4 and datetime.now().hour < 22:
        return '晚安呢~你的作息很规律呢~ ⁽⁽꜀(:3꜂ ꜆)꜄⁾⁾'
    if datetime.now().hour > 4 and datetime.now().hour < 24:
        return '晚安啦~祝你今晚好梦哟~ (›´ω`‹ )'
    if datetime.now().hour < 1:
        return '晚安啦~连菜菜都困了~明天你也要早一点休息哦~ (๑´0`๑)'
    if datetime.now().hour < 4:
        return '请快去睡觉！一定要保证好自己的身体！菜菜会担心的！Σ( ° △ °|||)︴'


next_fuck_time = 0
noticed = False


def say_hentai():
    global next_fuck_time
    global noticed
    from time import time
    from random import randint
    if time() < next_fuck_time:
        if noticed == False:
            noticed = True
            return '咦惹！不是刚日过嘛！'
        return ''
    next_fuck_time = time() + randint(450, 900)
    noticed = False
    result = randint(1, 20)
    if result == 1:
        return '欸嘿嘿嘿 来了来了|˛˙꒳​˙)♡'
    elif result == 2:
        return '唔……要轻点哦ꈍ◡ꈍ'
    elif result == 3:
        return '哼唧！'
    elif result == 4:
        return '不要……你的太大了……会痛的(o｀ε´o)'
    else:
        return 'hentai！离本菜远点！'
