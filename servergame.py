def Match(all_player,revealed_cards):
    all_player = all_player % 13
    revealed_cards = revealed_cards % 13
    if(all_player == 0):
        all_player = 13
    if(revealed_cards == 0):
        revealed_cards = 13
    if(all_player == revealed_cards and all_player in (10 ,11, 12, 13)):
        return True 
    elif(all_player + revealed_cards == 10): 
        return True
    else:
        return False

def is_red(player_card):
    if(player_card < 27):
        return True
    else:
        return False

def PlayerScore(reveal,player):
    sum = 0
    if is_red (reveal):
        reveal %= 13
        if(player % 13 == 0):
            reveal = 13
        sum +=  reveal 
    if is_red (player):
        player %=13
        if(player % 13 == 0):
            player = 13
        sum += player
    return sum

def show_score(a,score):
    print("player %d score %2d" %(a ,score[a]))