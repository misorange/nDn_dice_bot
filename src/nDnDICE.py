# coding: utf-8
import random
import re

pattern = '\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}'
split_pattern = 'd|D'

# 対象の文字列かどうか
def judge_nDn(src):
    repatter = re.compile(pattern)
    result = repatter.fullmatch(src)
    if result is not None:
        return True
    return False

# 何面ダイスを何回振るか
def split_nDn(src):
    return re.split(split_pattern,src)

# ダイスを振る
def role_nDn(src):
    result = []
    sum_dice = 0
    role_index = split_nDn(src)
    role_count = int(role_index[0])
    nDice = int(role_index[1])
    
    for i in range(role_count):
        tmp = random.randint(1,nDice)
        result.append(tmp)
        sum_dice = sum_dice + tmp
    
    is1dice = True if role_count == 1 else False
    
    return result,sum_dice,is1dice

def nDn(text):
    if judge_nDn(text):
        result,sum_dice,is1dice = role_nDn(text)
        if is1dice:
            return 'ダイス：' + text + '\n出目：' + str(sum_dice)
        else:
            return 'ダイス：' + text + '\n出目：' + str(result) + '\n合計：' + str(sum_dice)
    else:
        return None