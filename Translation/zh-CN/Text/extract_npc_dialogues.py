#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整NPC对话提取脚本
从多个源文件中提取NPC对话并写入到fallout_shelter_zh_NPCs.txt
"""

import os
import re
import sys
import glob

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def get_npc_patterns():
    """返回NPC对话的识别模式"""
    return [
        # 巧手先生对话模式
        r'^I never did understand',
        r'^You humans relax',
        r'^BlamCo',
        r'^Thank Heavens',
        r'^Ahhh, education',
        r'^Ah, cardio',
        r'^Hmph',
        r'^If the humans are happy',
        r'^So many humans',
        r'^Entombed in cold',
        r'^My kingdom for',
        r'^If I\'ve told',
        r'^Do this, do that',
        r'^Yes, Overseer',
        r'^I am a Mister',
        r'^Not a day goes by',
        r'^Live to serve',
        r'^Coming, coming',
        r'^They don\'t call me',
        r'^Hello, humans',
        r'^What do you need',
        r'^Now now, I don\'t',
        r'^Feeling lazy',
        r'^I\'ll do whatever',
        r'^Sometimes these humans',
        r'^I have to admit',
        r'^Oh look, a layer',
        r'^Joke time',
        r'^You hear about',
        r'^They say there',
        r'^Before the blasted',
        r'^What\'s on the agenda',
        r'^Have hover unit',
        r'^Personally, I think',
        r'^I do hope there\'s',
        r'^Is that',
        r'^There\'s not enough',
        r'^Ugh',
        r'^I wonder if we',
        r'^These humans can',
        r'^Hard work is',
        r'^Dinner tonight',
        r'^Olfactory sensors',
        r'^I do hope the humans',
        r'^This place could',
        r'^As soon as I get',
        r'^And so the humans',
        r'^Anyone fancy a tipple',
        r'^Oh my\. I certainly',
        r'^Send the robot',
        r'^If I go home',
        r'^If I were human',
        r'^My radiation sensors',
        r'^You know, it\'s',
        r'^A deflated basketball',
        r'^Oh look\. A destroyed',
        r'^Ah, the Wasteland',
        r'^My thermometer',
        r'^Looks like it may',
        r'^Rock in the road',
        r'^For an emotionless',
        r'^Hello! Yes you',
        r'^Sensors indicate',
        r'^And to think',
        r'^Of course',
        r'^If my makers',
        r'^Hellllloooo',
        r'^Ah, a broken bridge',
        r'^My goodness',
        r'^I think I\'m getting',
        r'^Don\'t mind me',
        r'^I want to go home',
        r'^Should I head back',
        r'^A domestic robot',
        r'^Definitely starting',
        r'^Send the robot, they',
        r'^I\'ll find what',
        r'^Agh! A Deathclaw',
        r'^Oh look\. A Feral',
        r'^Mole rat holes',
        r'^Hmm\. Large humans',
        r'^Hmm\. A chest',
        r'^Hmm\? Something',
        r'^Hmm\.\.\. Subway',
        r'^Hmm\.\.\. Broken',
        r'^Hmm\. Something',
        r'^Looks like a trail',
        r'^What luck',
        r'^Whoa',
        r'^Thirsty',
        r'^Oh good, this',
        r'^Ah\. So that\'s',
        r'^Uh oh',
        r'^I wonder how high',
        r'^Anybody need help',
        r'^Don\'t mind me, I\'ll',
        r'^So this is where',
        r'\*Sigh\*',
        r'^Imagine',
        r'^Anybody need me',
        r'^Mic check',
        r'^Oh, yes, let\'s',
        r'^Because, really',
        r'^Having to manage',
        r'^Oh my\. Isn\'t',
        r'^Surely someone',
        r'^Oh look, a broken',
        r'^I do hope there\'s no',
        r'^I do hope the humans',
        r'^I have to admit',
        r'^Olfactory sensors picking up',
        r'^This place could',
        r'^As soon as',
        r'^And so the',
        r'^I see a long',
        r'^So many humans seek',
        r'^The lighting in',
        r'^I wonder if the kitchen',
        r'^You humans are',
        r'^I wonder how',
        r'^Some of you',
        r'^That\'s it, humans',
        r'^Imagine',
        r'^Anybody need me',
        r'^Mic check, mic',
        r'^Oh, yes, let\'s',
        r'^Because, really',
        r'^Having to manage',
        r'^Oh my\. Isn\'t',
        r'^Surely someone',
        r'^Oh look, a broken',
        r'^I do hope there\'s',
        r'^I do hope the humans',
        r'^Is that\? Why yes',
        # 额外的NPC特征模式
        r'^Anybody need',
        r'^Don\'t mind me',
        r'^So this is',
        r'\*Sigh\*',
        r'^Imagine',
        r'^Because, really',
        r'^Having to',
        r'^Oh my',
        r'^Surely someone',
        # 废土探索者模式
        r'^Hmm',
        r'^Thirsty',
        r'^Whoa',
        r'^What luck',
        r'^Uh oh',
        # 机器人反应模式
        r'^Agh!',
        r'^Oh look',
        r'^Sensors',
        r'^My',
    ]

def is_npc_dialogue(line, patterns):
    """判断一行是否是NPC对话"""
    if not line.strip() or '=' not in line:
        return False

    english_part = line.split('=')[0].strip()

    # 检查是否匹配任何NPC模式
    for pattern in patterns:
        if re.match(pattern, english_part, re.IGNORECASE):
            return True

    # 检查特定的NPC特征（更精确）
    npc_indicators = [
        ' humans ', ' robot', ' Mister', ' Overseer', ' Wasteland ',
        ' Deathclaw', ' Super Mutant', ' Feral Ghoul', ' Mole rat',
        ' I never', ' I wonder', ' I think', ' I hope', ' I am',
        ' You humans', ' My ', ' Your ',
        # 特定的NPC表达
        'I never did understand', 'You humans relax', 'BlamCo',
        'Thank Heavens', 'Ahhh', 'Ah, cardio', 'Hmph',
        'Coming, coming', 'Hello, humans', 'Now now',
        'Joke time', 'Before the blasted', 'Have hover',
        'Personally, I', 'I do hope', 'There\'s not',
        'I wonder if', 'These humans', 'Hard work',
        'Olfactory sensors', 'This place', 'As soon as',
        'Anyone fancy', 'Send the robot', 'If I go',
        'If I were', 'My radiation', 'You know',
        'A deflated', 'Ah, the Wasteland', 'My thermometer',
        'Looks like', 'Rock in', 'For an emotionless',
        'Hello! Yes', 'Sensors indicate', 'And to think',
        'Of course', 'If my makers', 'Hellllloooo',
        'Ah, a broken', 'My goodness', 'I think I\'m',
        'Don\'t mind', 'I want to', 'Should I head',
        'A domestic', 'Definitely', 'Agh! A',
        'Oh look. A', 'Mole rat', 'Hmm. Large',
        'Hmm. A chest', 'Hmm? Something', 'Hmm... Subway',
        'Hmm... Broken', 'Hmm. Something', 'Looks like a trail',
        'What luck', 'Whoa!', 'Thirsty', 'Oh good, this',
        'Ah. So that\'s', 'Uh oh!', 'I wonder how',
        'Anybody need', 'Don\'t mind me, I\'ll', 'So this is',
        '*Sigh*', 'Imagine.', 'Anybody need me', 'Mic check',
        'Oh, yes, let\'s', 'Because, really', 'Having to manage',
        'Oh my. Isn\'t', 'Surely someone', 'Oh look, a broken',
        'I do hope there\'s', 'I do hope the humans',
    ]

    # 排除明显的非NPC对话（提示、说明等）
    non_npc_patterns = [
        r'^Hint:',
        r'^- ',
        r'^\d+\. ',
        r'^Tap ',
        r'^Click ',
        r'^Press ',
        r'^You must have',
        r'^The ',
        r'^This ',
        r'^That ',
        r'^Your ',
        r'^To ',
        r'^For ',
        r'^With ',
        r'^From ',
        r'^About ',
        r'^When ',
        r'^Where ',
        r'^Why ',
        r'^How ',
    ]

    # 检查是否是非NPC模式
    for pattern in non_npc_patterns:
        if re.match(pattern, english_part, re.IGNORECASE):
            return False

    # 检查是否包含NPC特征
    for indicator in npc_indicators:
        if indicator in english_part:
            return True

    return False

def extract_from_file(filepath, patterns):
    """从单个文件中提取NPC对话"""
    npc_dialogues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            stripped_line = line.strip()
            if stripped_line and is_npc_dialogue(stripped_line, patterns):
                npc_dialogues.append(stripped_line)

    except Exception as e:
        print(f"  读取文件错误: {e}")

    return npc_dialogues

def extract_all_npc_dialogues(base_path, patterns):
    """从所有翻译文件中提取NPC对话"""
    all_npc_dialogues = []

    # 要搜索的文件
    search_files = [
        "fallout_shelter_zh_story.txt",
        "fallout_shelter_zh_Tutorial.txt",
        "_Substitutions.txt",
        "_Postprocessors.txt"
    ]

    print("正在从以下文件中提取NPC对话:")
    for filename in search_files:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            print(f"  - {filename}")
            npc_dialogues = extract_from_file(filepath, patterns)
            all_npc_dialogues.extend(npc_dialogues)
            print(f"    提取到: {len(npc_dialogues)} 条")
        else:
            print(f"  - {filename} (文件不存在)")

    return all_npc_dialogues

def write_npc_file(npc_file, npc_dialogues):
    """写入NPC文件"""
    # 去重并保持顺序
    unique_dialogues = []
    seen = set()
    for dialogue in npc_dialogues:
        if dialogue not in seen:
            seen.add(dialogue)
            unique_dialogues.append(dialogue)

    with open(npc_file, 'w', encoding='utf-8') as f:
        for dialogue in unique_dialogues:
            f.write(dialogue + '\n')

    return len(unique_dialogues)

def main():
    # 文件路径
    base_path = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text"
    npc_file = os.path.join(base_path, "fallout_shelter_zh_NPCs.txt")

    print("=== NPC对话提取脚本 ===")
    print(f"基础路径: {base_path}")
    print(f"NPC文件: {npc_file}")
    print()

    # 获取NPC识别模式
    patterns = get_npc_patterns()
    print(f"NPC识别模式数量: {len(patterns)}")
    print()

    # 提取所有NPC对话
    npc_dialogues = extract_all_npc_dialogues(base_path, patterns)

    print(f"总共提取到NPC对话: {len(npc_dialogues)} 条")
    print()

    # 写入NPC文件
    print("正在写入NPC文件...")
    unique_npc_count = write_npc_file(npc_file, npc_dialogues)
    print(f"写入NPC文件（去重后）: {unique_npc_count} 条")

    print()
    print("=== 处理完成 ===")
    print(f"NPC对话总数: {len(npc_dialogues)} 条")
    print(f"去重后数量: {unique_npc_count} 条")
    print(f"重复数量: {len(npc_dialogues) - unique_npc_count} 条")

    # 显示示例
    print()
    print("=== NPC对话示例 ===")
    with open(npc_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:10], 1):
            print(f"{i}. {line[:80]}")

    print()
    print("提取完成！")

if __name__ == "__main__":
    main()