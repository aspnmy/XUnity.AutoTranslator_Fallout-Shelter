#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超精确NPC对话识别脚本
"""

import os
import re
import sys

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def is_pure_dialogue(line):
    """判断是否为纯粹的角色对话"""
    if not line.strip() or '=' not in line:
        return False

    english_part = line.split('=')[0].strip()

    # 排除系统提示和叙述内容
    system_patterns = [
        r'one of your',
        r'Your (Dweller|Vault|Quest team)',
        r'While exploring',
        r'We have word that',
        r'Dwellers out in',
        r'Congratulations! Vault-Tec',
        r'Now that you know',
        r'Great! You created',
        r'^Hint:',
        r'^\d+\. ',
        r'^- ',
    ]

    for pattern in system_patterns:
        if re.search(pattern, english_part, re.IGNORECASE):
            return False

    # 纯对话特征
    dialogue_features = [
        # 第一人称
        r'^I (am|was|will|think|hope|wonder|want|need|have|had|feel|know|see|hear|said|told|asked|answered)',
        r'^I\'(m|ve|d|ll) ',

        # 直接称呼和互动
        r'^(Hey|Hello|Hi|Excuse|Thank|Be careful|Watch out)',
        r'^(Yes|No|Oh|Ah|Ugh|Hmm|Hmph|Agh|Whoa)',

        # 疑问句
        r'\?$',

        # 情感表达
        r'^(Ha ha|Heh|Hmph|\*Sigh\*)',

        # 角色身份表达
        r'^I am (the|a|Dr\.|Mr\.|Mrs\.)',
        r'^I\'m (the|a|Dr\.|Mr\.|Mrs\.)',

        # 对话标记
        r'^"',
    ]

    for feature in dialogue_features:
        if re.match(feature, english_part, re.IGNORECASE):
            return True

    return False

def final_cleanup():
    """最终清理"""
    npc_file = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text\fallout_shelter_zh_NPCs.txt"

    pure_dialogue = []
    system_messages = []

    with open(npc_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line and '=' in line:
            if is_pure_dialogue(line):
                pure_dialogue.append(line)
            else:
                system_messages.append(line)

    # 写入纯对话文件
    with open(npc_file, 'w', encoding='utf-8') as f:
        for line in sorted(set(pure_dialogue)):
            f.write(line + '\n')

    # 保存系统消息到临时文件
    temp_file = r"e:\SteamLibrary\steamapps\common\Fallout Shelter\BepInEx\Translation\zh-CN\Text\system_messages.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        for line in sorted(set(system_messages)):
            f.write(line + '\n')

    return len(pure_dialogue), len(system_messages)

def main():
    print("=== 超精确NPC对话清理 ===")
    print()

    dialogue_count, system_count = final_cleanup()

    print(f"保留的纯对话: {dialogue_count} 条")
    print(f"移除的系统消息: {system_count} 条")
    print()

    print("清理完成！")

if __name__ == "__main__":
    main()