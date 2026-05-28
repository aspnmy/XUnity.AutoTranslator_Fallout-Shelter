#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确NPC对话识别和分类脚本
"""

import os
import re
import sys

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def is_true_npc_dialogue(line):
    """判断是否为真正的NPC对话"""
    if not line.strip() or '=' not in line:
        return False

    english_part = line.split('=')[0].strip()

    # 真正NPC对话的特征模式
    npc_dialogue_patterns = [
        # 第一人称表达
        r'^I (never|think|hope|wonder|don\'t|can\'t|have|am|was|will|would|should)',
        r'^I\'(m|ve|d|ll) ',
        r'^My (kingdom|radiation|goodness|thermometer|internal|name)',
        r'^We (don\'t|can\'t|have|are|were)',
        r'^Our (Vault|home|place)',

        # 情感表达和语气词
        r'^(Oh|Ah|Ugh|Hmm|Hmph|Yaaawwn|Agh|Whoa|Yes|No|Hey|Hello)',
        r'^\*Sigh\*',
        r'^Ha ha ha',
        r'^Heh|嘿嘿|哈哈|呵呵',

        # 特定角色表达
        r'^You humans',
        r'^Coming, coming',
        r'^Live to serve',
        r'^They don\'t call me',
        r'^Hello, humans',
        r'^Now now, I',
        r'^Feeling lazy',
        r'^Sometimes these humans',
        r'^I have to admit',
        r'^Personally, I',
        r'^I do hope',
        r'^There\'s not',
        r'^This place',
        r'^As soon as',
        r'^And so the',
        r'^Anyone fancy',
        r'^Send the robot',
        r'^If I go',
        r'^If I were',
        r'^You know, it\'s',
        r'^A deflated',
        r'^My radiation',
        r'^Ah, the Wasteland',
        r'^My thermometer',
        r'^Looks like',
        r'^Rock in',
        r'^For an emotionless',
        r'^Hello! Yes',
        r'^Sensors indicate',
        r'^And to think',
        r'^Of course',
        r'^If my makers',
        r'^Hellllloooo',
        r'^My goodness',
        r'^I think I\'m',
        r'^Don\'t mind',
        r'^I want to',
        r'^Should I head',
        r'^A domestic',
        r'^Definitely',
        r'^I\'ll find',
        r'^Agh! A',
        r'^Oh look. A',
        r'^Mole rat',
        r'^Hmm. (Large|A chest|Something)',
        r'^Hmm\.\.\. (Subway|Broken)',
        r'^Looks like a',
        r'^What luck',
        r'^Thirsty',
        r'^Oh good',
        r'^Uh oh',
        r'^So this is',
        r'^Imagine',
        r'^Anybody need',
        r'^Because, really',
        r'^Having to',
        r'^Surely someone',

        # 巧手先生特定表达
        r'^Mister Handy',
        r'^General Atomics',
        r'^robot humor',
        r'^oil bath',
        r'^hover unit',
        r'^bloody',
        r'^for Heaven\'s sake',

        # 对话和互动特征
        r'^Excuse me',
        r'^Pardon me',
        r'^Thank you',
        r'^You\'re welcome',
        r'^Good luck',
        r'^Be careful',
        r'^Watch out',
        r'^Hurry up',
        r'^Wait a minute',
    ]

    # 检查是否匹配NPC对话模式
    for pattern in npc_dialogue_patterns:
        if re.match(pattern, english_part, re.IGNORECASE):
            return True

    return False

def classify_content(line):
    """对内容进行分类"""
    if not line.strip() or '=' not in line:
        return 'other'

    english_part = line.split('=')[0].strip()

    # 任务目标/成就描述
    objective_patterns = [
        r'^Have \d+ ',
        r'^Complete \d+ ',
        r'^Kill \d+ ',
        r'^Collect \d+ ',
        r'^Craft \d+ ',
        r'^Equip \d+ ',
        r'^Send \d+ ',
        r'^Build \d+ ',
        r'^Upgrade \d+ ',
        r'^Survive \d+ ',
        r'^Reach level \d+ ',
        r'^Find \d+ ',
        r'^Use \d+ ',
        r'^Sell \d+ ',
        r'^Buy \d+ ',
    ]

    for pattern in objective_patterns:
        if re.match(pattern, english_part):
            return 'objective'

    # 物品描述
    item_patterns = [
        r'^Great at keeping',
        r'^Probably more useful',
        r'^A favorite of',
        r'^Gumshoe gear',
        r'^Greet the',
        r'^Functional and flattering',
        r'^Make lists',
        r'^Offers great protection',
        r'^Handle anything',
        r'^Institute-sanctioned',
        r'^Usually reserved for',
        r'^An indoor cat',
        r'^Loves keeping',
        r'^Looks like he\'s',
        r'^Can sing',
    ]

    for pattern in item_patterns:
        if re.match(pattern, english_part):
            return 'item'

    # 系统提示
    system_patterns = [
        r'^One of your Dwellers',
        r'^Your (Dweller|Vault)',
        r'^You should',
        r'^You must',
        r'^You can',
        r'^You\'ve already',
        r'^Dwellers out in',
        r'^A Wasteland explorer',
        r'^Congratulations! Vault-Tec',
        r'^Now that you know',
        r'^Great! You created',
    ]

    for pattern in system_patterns:
        if re.match(pattern, english_part):
            return 'system'

    # 检查是否是真正的NPC对话
    if is_true_npc_dialogue(line):
        return 'npc'

    # 可正则化的内容（包含数字）
    if re.search(r'\d+', english_part) and re.search(r'(day|hour|minute|second|time|level|point|percent|count)', english_part, re.IGNORECASE):
        return 'regex'

    return 'other'

def process_npc_file():
    """处理NPC文件，分类内容"""
    npc_file = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text\fallout_shelter_zh_NPCs.txt"

    categories = {
        'npc': [],
        'objective': [],
        'item': [],
        'system': [],
        'regex': [],
        'other': []
    }

    with open(npc_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                category = classify_content(line)
                categories[category].append(line)

    return categories

def main():
    print("=== NPC文件内容分类 ===")
    print()

    categories = process_npc_file()

    for category, lines in categories.items():
        if lines:
            print(f"{category.upper()}: {len(lines)} 条")
            if len(lines) <= 5:
                for line in lines:
                    print(f"  {line[:80]}")
            else:
                for line in lines[:3]:
                    print(f"  {line[:80]}")
                print(f"  ... 还有 {len(lines)-3} 条")
            print()

    # 统计
    total = sum(len(lines) for lines in categories.values())
    npc_count = len(categories['npc'])
    non_npc_count = total - npc_count

    print(f"总计: {total} 条")
    print(f"NPC对话: {npc_count} 条 ({npc_count/total*100:.1f}%)")
    print(f"非NPC内容: {non_npc_count} 条 ({non_npc_count/total*100:.1f}%)")

if __name__ == "__main__":
    main()