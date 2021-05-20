import json

bot_id = '2485909839'
morning_dict = {}
night_dict = {}

def save_dict():
    # 计算时间 6点以前算前一天！
    from datetime import datetime
    from datetime import timedelta
    now_time = datetime.now()
    if now_time.hour < 6:
        now_time = now_time - timedelta(days=1)
    now_date = datetime.date(now_time)
    
    # 保存早晚json
    global morning_dict
    global night_dict
    file_name = './datebase/morning/morning_dict ' + now_date.__str__() + '.json'
    f = open(file_name, 'w')
    f.write(json.dumps(morning_dict))
    f.close()
    file_name = './datebase/morning/night_dict ' + now_date.__str__() + '.json'
    f = open(file_name, 'w')
    f.write(json.dumps(night_dict))
    f.close()

    # 每早6点清空数据
    from datetime import datetime
    now_time = datetime.now()
    if now_time.hour == 6 and now_time.minute == 0:
        morning_dict = {}
        night_dict = {}

def load_dict():
    from datetime import datetime
    from datetime import timedelta
    now_time = datetime.now()
    if now_time.hour < 6:
        now_time = now_time - timedelta(days=1)
    now_date = datetime.date(now_time)

    file_name = './datebase/morning/morning_dict ' + now_date.__str__() + '.json'
    try:
        with open(file_name, 'r') as f:
            flie_content = f.read()
            global morning_dict
            morning_dict = json.loads(flie_content)
            f.close()
    except IOError:
        pass

    file_name = './datebase/morning/night_dict ' + now_date.__str__() + '.json'
    try:
        with open(file_name, 'r') as f:
            flie_content = f.read()
            global night_dict
            night_dict = json.loads(flie_content)
            f.close()
    except IOError:
        pass
