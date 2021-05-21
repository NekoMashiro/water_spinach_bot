total_card = []
player = 0
finished_player = 0
every_player_card = {}
every_player_point = {}


def card_game_start():
    global total_card
    global player
    global finished_player

    player = 0
    finished_player = 0
    total_card = random_card_list()

    every_player_card.clear()
    every_player_card['banker'] = []
    every_player_card['banker'].append(total_card.pop())
    every_player_card['banker'].append(total_card.pop())
    first_card = card_to_string(every_player_card['banker'][0])

    str = '菜菜的第一张牌是' + first_card + '哦 '
    if(every_player_card['banker'][0][1] == 1):
        str += '好像很危险耶Σ(ﾟ∀ﾟﾉ)ﾉ '
    str += '至于第二张牌……可不能告诉你呢！'
    return str


def add_player(player_id):
    global player
    player = player + 1
    every_player_card[player_id] = []
    every_player_card[player_id].append(total_card.pop())
    every_player_card[player_id].append(total_card.pop())

    str = '你的初始手牌是：'
    for card in every_player_card[player_id]:
        str += card_to_string(card) + ' '
    str += calc_handcards_point(player_id)
    return str


def stop_card(player_id):
    global player
    global finished_player
    finished_player = finished_player + 1
    if player == finished_player:
        return True
    return False


def ask_card(player_id):
    every_player_card[player_id].append(total_card.pop())
    handcards = every_player_card[player_id].copy()

    str = '你的手牌是：'
    for card in handcards:
        str += card_to_string(card) + ' '
    str += calc_handcards_point(player_id)
    return str


def calc_handcards_point(player_id):
    handcards = every_player_card[player_id]
    point = 0
    num_a = 0
    for card in handcards:
        if card[1] > 10:
            point += 10
        else:
            point += card[1]
        if card[1] == 1:
            num_a = num_a + 1
    while point <= 10 and num_a != 0:
        point += 11
        num_a -= 1

    if point > 21:
        every_player_point[player_id] = -1
        return '总点数是……' + point.__str__() + '…………爆掉了(°ー°〃)'

    if len(handcards) == 2 and point == 21:
        every_player_point[player_id] = 22
        return '是Black Jack诶Σ(ﾟ∀ﾟﾉ)ﾉ'

    every_player_point[player_id] = point
    return '总点数是' + point.__str__() + '点哦'


def card_to_string(card: tuple):
    str = ''
    if card[0] == 1:
        str += '♠'
    elif card[0] == 2:
        str += '♥'
    elif card[0] == 3:
        str += '♣'
    elif card[0] == 4:
        str += '♦'

    if card[1] == 1:
        str += 'A'
    elif card[1] == 11:
        str += 'J'
    elif card[1] == 12:
        str += 'Q'
    elif card[1] == 13:
        str += 'K'
    else:
        str += card[1].__str__()
    return str


def random_card_list():
    l = []
    total = 0
    for i in range(1, 5):
        for j in range(1, 14):
            from random import randint
            pos = randint(0, total)
            total = total + 1
            l.insert(pos, (i, j))
    return l


def final_calc():
    pass
