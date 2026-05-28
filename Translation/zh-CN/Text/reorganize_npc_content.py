#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新分类和移动NPC文件内容脚本
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
        r'^I (never|think|hope|wonder|don\'t|can\'t|have|am|was|will|would|should)',
        r'^I\'(m|ve|d|ll) ',
        r'^My (kingdom|radiation|goodness|thermometer|internal|name)',
        r'^We (don\'t|can\'t|have|are|were)',
        r'^Our (Vault|home|place)',

        # 情感表达和语气词
        r'^(Oh|Ah|Ugh|Hmm|Hmph|Yaaawwn|Agh|Whoa|Yes|No|Hey|Hello)',
        r'^\*Sigh\*',
        r'^Ha ha ha',
        r'^Heh',

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

        # 另外一些明确的NPC对话模式
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
        r'^What do you need',
        r'^Joke time',
        r'^You hear about',
        r'^They say there',
        r'^Before the blasted',
        r'^What\'s on the agenda',
        r'^Have hover unit',
        r'^Is that',
        r'^I wonder if',
        r'^These humans can',
        r'^Hard work is',
        r'^Dinner tonight',
        r'^Olfactory sensors',
        r'^I do hope the humans',
    ]

    # 检查是否匹配NPC对话模式
    for pattern in npc_dialogue_patterns:
        if re.match(pattern, english_part, re.IGNORECASE):
            return True

    return False

def make_regex_pattern(line):
    """将数字替换为正则表达式"""
    english, chinese = line.split('=', 1)
    english = english.strip()
    chinese = chinese.strip()

    # 替换数字为{#}或\d+
    english_regex = re.sub(r'(\d+)', r'{#}', english)
    chinese_regex = re.sub(r'(\d+)', r'$1', chinese)

    return f"{english_regex}={chinese_regex}"

def reorganize_content():
    """重新组织内容"""
    base_path = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text"

    npc_file = os.path.join(base_path, "fallout_shelter_zh_NPCs.txt")
    story_file = os.path.join(base_path, "fallout_shelter_zh_story.txt")
    substitutions_file = os.path.join(base_path, "_Substitutions.txt")
    tutorial_file = os.path.join(base_path, "fallout_shelter_zh_Tutorial.txt")

    # 读取当前NPC文件内容
    with open(npc_file, 'r', encoding='utf-8') as f:
        npc_lines = [line.strip() for line in f if line.strip() and '=' in line]

    # 分类内容
    true_npc = []
    return_to_story = []
    add_to_substitutions = []
    add_to_tutorial = []

    for line in npc_lines:
        if is_true_npc_dialogue(line):
            true_npc.append(line)
        else:
            english_part = line.split('=')[0].strip()

            # 检查是否包含数字（可能是可正则化的任务目标）
            if re.search(r'\d+', english_part):
                regex_line = make_regex_pattern(line)
                add_to_substitutions.append(regex_line)
            # 系统提示和教程内容
            elif re.search(r'(Congratulations|Dwellers out|One of your|You should|You must|You can|Great! You created|Now that you know)', english_part, re.IGNORECASE):
                return_to_story.append(line)
            # 物品描述
            elif re.search(r'(Great at keeping|Probably more useful|A favorite of|Gumshoe gear|Functional|Offers great|Handle anything|Institute-sanctioned|Usually reserved|Loves keeping|Looks like he|Can sing)', english_part, re.IGNORECASE):
                return_to_story.append(line)
            # 其他非NPC内容
            else:
                return_to_story.append(line)

    # 写入真正的NPC文件
    with open(npc_file, 'w', encoding='utf-8') as f:
        for line in sorted(set(true_npc)):
            f.write(line + '\n')

    # 读取并追加到story文件
    if return_to_story:
        with open(story_file, 'a', encoding='utf-8') as f:
            for line in sorted(set(return_to_story)):
                f.write(line + '\n')

    # 追加到substitutions文件
    if add_to_substitutions:
        with open(substitutions_file, 'a', encoding='utf-8') as f:
            for line in sorted(set(add_to_substitutions)):
                f.write(line + '\n')

    return {
        'npc': len(true_npc),
        'story': len(return_to_story),
        'substitutions': len(add_to_substitutions),
        'total': len(npc_lines)
    }

def main():
    print("=== 重新组织NPC文件内容 ===")
    print()

    result = reorganize_content()

    print(f"原始NPC文件: {result['total']} 条")
    print(f"真正的NPC对话: {result['npc']} 条")
    print(f"返回Story文件: {result['story']} 条")
    print(f"添加到Substitutions: {result['substitutions']} 条")
    print()

    print("重新组织完成！")

if __name__ == "__main__":
    main()